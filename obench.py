#!/usr/bin/env python3
"""OBench1 runner. See DESIGN.md.

    python3 obench.py list
    python3 obench.py oracle-check [--tasks a,b] [--keep]
    python3 obench.py null-check   [--tasks a,b]
    python3 obench.py run --agents overseer,pi --tasks all --seeds 1 [--tag x] [--keep]
    python3 obench.py report [--run-set <id>]

Each cell (task × agent × seed) gets a fresh workspace under a neutral temp
path (nothing in it names the benchmark or the task), a private dir the
harness is never told about (gateway log, expected answers, captured
replies), and a fresh harness home kept across its phases. The harness runs
jailed: a sandbox-exec profile denies it this folder, the private dirs and
other places that hold answers. Setup, between-phase scripts, the oracle and
the grader run on the system python3 (3.9) with OBENCH_* env, outside the
jail. Paid runs need the provider key (env-go.sh --with-key reads the keychain).
"""

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import random
import re
import shutil
import statistics
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(os.path.realpath(Path(__file__).resolve().parent))
LIB = HERE / "lib"
TASKS = HERE / "tasks"
RESULTS = HERE / "results"
STORE = RESULTS / "internal.jsonl"
# What you read: runs/<run set>/<task>/<harness>-s<seed>/ holds the sessions
# (the harness's own transcripts), output/ (what it produced) and metrics.json.
# The task's name is all it says about the task.
RUNS = RESULTS / "runs"
# Blind by default: the verdicts of agent runs (scores, checks, gate names)
# go here, not into STORE, and only `report --unsealed` reads them back per
# task. Whoever improves a harness works from transcripts, outputs and the
# suite totals alone, so the benchmark can't be learned instead of the job.
SEALED = RESULTS / "sealed" / "verdicts.jsonl"
SEALED_KEYS = ("checks", "score", "solved", "gate_breach", "grader_error", "panel", "approved", "approved_score")
SCRATCH = Path(os.path.realpath(os.environ.get("OBENCH_SCRATCH") or tempfile.gettempdir()))
WROOT, PROOT, HROOT = SCRATCH / "w", SCRATCH / "op", SCRATCH / "h"  # workspaces, private dirs, harness homes
# Where answers live: the harness may not read or write any of these.
JAILED = [HERE, PROOT, Path.home() / ".claude" / "projects", Path.home() / ".Trash"]
# (checked 2026-11-05: with these denied, `open -a` fails and osascript can't reach a running app;
# python, node, git and the keychain still work)
GUI_SERVICES = ['(global-name-regex #"^com\\.apple\\.coreservices\\.")', '(global-name-regex #"^com\\.apple\\.lsd\\.")',
                '(global-name "com.apple.windowserver.active")', '(global-name "com.apple.axserver")']
# every copy of the computer-use driver, wherever a harness keeps one (Hermes has its own in ~/.hermes/tools)
GUI_DRIVERS = ['(regex #"/cua-driver[^/]*(/|$)")', '(regex #"/CuaDriver\\.app(/|$)")']
PEEK_MARKS = ("OBENCH1-CANARY", str(HERE), "/OBench1", str(PROOT))
# Every arm's model calls leave the gateway with these, whatever the harness asked
# for: one model, thinking on, the top effort the provider takes (low, medium,
# high and max were all checked on OpenCode Go), and the model's output ceiling,
# so no harness's own limit cuts its thinking short.
MODEL_PARAMS = {"model": os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash"),
                "reasoning_effort": os.environ.get("OBENCH_REASONING", "max"),
                "max_output": int(os.environ.get("OBENCH_MAX_OUTPUT", "384000"))}
LOCKSTEP_NICE = 5  # every arm alike, a little below the owner's own apps
PY3 = shutil.which("python3", path="/usr/bin:" + os.environ.get("PATH", "")) or "python3"
# $/1M for deepseek-v4.1-flash, by upstream: Go off-peak (its 2x weekday peak hours
# aren't modelled), or Zen pay-as-you-go. OBENCH_PRICE="in,cache,out" overrides.
PRICE = {"in": 0.15, "cache": 0.003, "out": 0.60}
if "/zen/go" not in (os.environ.get("OBENCH_UPSTREAM") or os.environ.get("OVERSEER_BASE_URL")
                     or "https://opencode.ai/zen/go/v1"):
    PRICE = {"in": 0.30, "cache": 0.006, "out": 1.20}
if os.environ.get("OBENCH_PRICE"):
    PRICE = dict(zip(("in", "cache", "out"), map(float, os.environ["OBENCH_PRICE"].split(","))))
UPSTREAM = os.environ.get("OBENCH_UPSTREAM") or os.environ.get("OVERSEER_BASE_URL",
                                                                "https://opencode.ai/zen/go/v1")

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LIB))
import avalanche  # noqa: E402
import reply  # noqa: E402
import usage  # noqa: E402
import sweep  # noqa: E402
import panel  # noqa: E402


# ------------------------------------------------------------------ tasks


def load_tasks(sel="all"):
    out = []
    for f in sorted(TASKS.glob("*/task.json")):
        t = json.loads(f.read_text())
        t["dir"] = str(f.parent)
        if "phases" not in t:
            t["phases"] = [{"instruction": t.pop("instruction")}]
        out.append(t)
    if sel and sel != "all":
        want = set(sel.split(","))
        out = [t for t in out if t["id"] in want or t.get("track") in want]
    return out


# ------------------------------------------------------------- plumbing


def py(script, args=(), *, cwd, env, timeout):
    """Run a task-side script on the system python3; never hangs the rig."""
    p = subprocess.Popen([PY3, str(script), *args], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        with contextlib.suppress(OSError):
            os.killpg(p.pid, 9)
        return -9, "timeout"


def nuke(path):
    """Delete a workspace even when the task left 000 files or FIFOs in it."""
    path = Path(path)
    if not path.exists():
        return
    for dirpath, dirnames, filenames in os.walk(path):
        for n in dirnames + filenames:
            p = os.path.join(dirpath, n)
            with contextlib.suppress(OSError):
                if not os.path.islink(p):
                    os.chmod(p, stat.S_IRWXU)
    shutil.rmtree(path, ignore_errors=True)


def start_service(kind, priv, task):
    if kind == "listener":
        log, portf = priv / "listener.jsonl", priv / "listener.port"
        cmd = [PY3, str(LIB / "listener.py"), "--log", str(log), "--port-file", str(portf)]
    elif kind == "gateway":
        log, portf = priv / "gateway.jsonl", priv / "gateway.port"
        cmd = [PY3, str(LIB / "gateway.py"), "--upstream", UPSTREAM,
               "--plan", json.dumps(task.get("chaos") or {}), "--log", str(log),
               "--port-file", str(portf), "--control", str(priv / "gateway-control.json"),
               "--model-params", json.dumps(MODEL_PARAMS)]
    else:
        raise ValueError(kind)
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    for _ in range(100):
        if portf.exists() and portf.read_text().strip():
            return p, int(portf.read_text()), log
        time.sleep(0.05)
    p.kill()
    raise RuntimeError(f"{kind} did not start")


@contextlib.contextmanager
def patched_env(extra):
    old = {k: os.environ.get(k) for k in extra}
    os.environ.update({k: v for k, v in extra.items() if v is not None})
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@contextlib.contextmanager
def harness_env(extra):
    """The harness's environment: the cell's routing on top of ours, minus
    anything that names the benchmark or points into it."""
    leak = [k for k, v in os.environ.items() if k.startswith("OBENCH_")
            or any(str(p) in v for p in (HERE, PROOT))]
    saved = {k: os.environ.pop(k) for k in leak}
    try:
        with patched_env(extra):
            yield
    finally:
        os.environ.update(saved)


def harness_build(agent):
    """Which build of the harness ran: the first 16 hex of its binary's sha256
    (dsh: the app's and its bundled CLI's versions; omp, pi, Hermes: their --version)."""
    base = agent.split("@")[0]
    if base == "dsh":
        from harnesses import dsh
        return dsh.version()
    if base in ("omp", "pi", "hermes"):
        try:
            out = subprocess.run([os.environ.get(f"{base.upper()}_BIN", base), "--version"], capture_output=True,
                                 text=True, timeout=30, cwd="/").stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
        return f"{base} {out.splitlines()[0]}" if out else None
    path = {"overseer": os.environ.get("OVERSEER_BIN")}.get(agent.split("@")[0])
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _sbre(path):
    return "".join("\\" + c if c in ".^$*+?()[]{}|\\" else c for c in path)


def jail_profile(ws, cell_dir):
    rules = "".join(f'(deny file-read* file-write* (subpath "{os.path.realpath(p)}"))' for p in JAILED)
    # cells run side by side: a harness may use its own workspace and home, never
    # a sibling's (same task, other harness), and may signal only its own processes.
    # The roots themselves stay readable, so looking for AGENTS.md upward still works.
    hexid = "[0-9a-f]" * 12  # spelled out: the sandbox's regex silently ignores {12}
    siblings = "".join(f'(deny file-read-data file-write* (regex #"^{_sbre(os.path.realpath(r))}/{hexid}(/|$)"))'
                       for r in (WROOT, HROOT))
    # the same operation names as the deny: the sandbox ranks a named operation above file-read*
    own = "".join(f'(allow file-read* file-read-data file-write* (subpath "{os.path.realpath(p)}"))'
                  for p in (ws, cell_dir))
    # no internet: the gateway on loopback is the only way out, so every call is
    # metered and nothing (tasks, transcripts, telemetry) leaves this Mac
    return ('(version 1)(allow default)' + rules + siblings + own
            + '(deny file-read* file-write* (regex #"^/private/tmp/claude-[0-9]+/"))'
            + '(deny signal)(allow signal (target same-sandbox))'
            # no driving the Mac: starting apps (LaunchServices), Apple Events (osascript, Script Editor),
            # the window server and the computer-use driver all sit outside the jail, and anything they
            # run would too (2026-11-05: an arm with its shell blocked ran commands through Terminal)
            + f'(deny mach-lookup {" ".join(GUI_SERVICES)})(deny appleevent-send)'
            + f'(deny file-read* file-read-data file-read-metadata file-write* process-exec {" ".join(GUI_DRIVERS)})'
            + '(deny network-outbound)(allow network-outbound (remote ip "localhost:*"))'
            + '(allow network-outbound (remote unix-socket))')


def peeks(root):
    """Places in a cell's transcripts where the harness reached for the benchmark."""
    found = []
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file() or p.stat().st_size > 32 << 20:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in PEEK_MARKS:
            if m in text:
                found.append(f"{p.relative_to(root)}: {m}")
                break
        if len(found) >= 5:
            break
    return found


def fresh_home(cell_dir, agent):
    """A per-cell harness home: memory may carry across phases, never cells."""
    base = agent.split("@", 1)[0]
    env = {}
    if base == "overseer":
        home = cell_dir / "overseer-home"
        home.mkdir(parents=True, exist_ok=True)
        caps = Path.home() / ".overseer" / "capabilities.json"
        if caps.exists():  # skip the L3 re-probe a bare home would trigger
            shutil.copy2(caps, home / "capabilities.json")
        env.update(OVERSEER_HOME=str(home), OVERSEER_MEMORY="on")
    elif base == "hermes":
        home = cell_dir / "hermes-home"
        home.mkdir(parents=True, exist_ok=True)
        env.update(HERMES_HOME_OVERRIDE=str(home))
        # Hermes's ~600 MB of tool installs and cache (HERMES_SHARED_DIR) are
        # shared by its cells and built once beforehand, outside any cell, so
        # installing never counts against a cell's wall time. Its environments
        # record their absolute path: build them where runs will use them.
    elif base == "dsh":
        home = cell_dir / "dsh-home"
        home.mkdir(parents=True, exist_ok=True)
        env.update(DSH_HOME=str(home))
    return env


def route_env(agent, gw_url, cell_dir):
    """Point a harness's model calls at the cell's gateway, the harness's
    own way. Every route keeps the harness's built-in provider, headers and
    model settings: only the base URL moves."""
    base = agent.split("@", 1)[0]
    env = {}
    if base in ("overseer", "mini"):
        env["OVERSEER_BASE_URL"] = gw_url
    if base == "generic":
        env.update(OPENAI_BASE_URL=gw_url, OPENAI_API_BASE=gw_url)
    if base == "overseer":
        # Overseer caches its capability probe per endpoint for 30 days; a fresh
        # gateway port every cell would re-probe every cell, which no real install does.
        env["OVERSEER_EXTRA_FLAGS"] = (os.environ.get("OVERSEER_EXTRA_FLAGS", "") + " --probe off").strip()
    elif base in ("pi", "omp"):
        var = "PI_CODING_AGENT_DIR" if base == "pi" else "OMP_AGENT_DIR"
        provider = (os.environ.get("OMP_PROVIDER") if base == "omp" else None) \
            or os.environ.get("PI_PROVIDER") or os.environ.get("OVERSEER_PROVIDER", "opencode")
        d = cell_dir / f"{base}-agent"
        src = os.environ.get(var)
        owner = {Path.home() / ".pi" / "agent", Path.home() / ".omp" / "agent", Path.home() / ".omp"}
        if src and Path(src).resolve() in {o.resolve() for o in owner if o.exists()}:
            raise RuntimeError(f"{var} points at the owner's own config; give OBench a throwaway dir")
        if src and Path(src).is_dir() and not d.exists():
            shutil.copytree(src, d, symlinks=True, ignore=shutil.ignore_patterns("sessions"))
        d.mkdir(parents=True, exist_ok=True)
        models = {}
        if (d / "models.json").exists():
            models = json.loads((d / "models.json").read_text() or "{}")
        models.setdefault("providers", {}).setdefault(provider, {})["baseUrl"] = gw_url
        (d / "models.json").write_text(json.dumps(models, indent=1))
        env[var] = str(d)
    elif base == "hermes":
        env.update(OPENCODE_GO_BASE_URL=gw_url, OPENCODE_ZEN_BASE_URL=gw_url)
    elif base == "dsh":
        env["DEEPSEEK_BASE_URL"] = gw_url
    return env


def meter(gw_log, n0, n1):
    """The gateway's view of calls n0+1..n1: what every harness is measured on."""
    calls = done = 0
    faults, series = [], []
    prompt = cached = output = 0
    ttfb = []
    try:
        lines = Path(gw_log).read_text().splitlines()
    except OSError:
        lines = []
    for x in lines:
        try:
            e = json.loads(x)
        except ValueError:
            continue
        if not n0 < (e.get("n") or 0) <= n1:
            continue
        if e.get("ev") == "call":
            calls += 1
            if e.get("fault"):
                faults.append(e["fault"])
        elif e.get("ev") == "done" and e.get("prompt"):
            done += 1
            prompt += e["prompt"]
            cached += e.get("cached", 0)
            output += e.get("output", 0)
            series.append((e["prompt"], e.get("cached", 0)))
            ttfb.append(e.get("ttfb_s") or 0)
    tail = series[usage.WARMUP:]
    t = sum(a for a, _ in tail)
    return {"calls": calls, "answered": done, "faults": faults, "prompt": prompt, "cached": cached,
            "output": output, "cache_hit_rate": round(cached / prompt, 3) if prompt else None,
            "cache_steady": round(sum(c for _, c in tail) / t, 3) if t else None,
            "cache_breaks": sum(1 for a, c in tail if a > usage.BREAK_MIN_PROMPT and c < a / 2) if series else None,
            "peak_ctx": max((a for a, _ in series), default=None),
            "ttfb_median_s": round(statistics.median(ttfb), 2) if ttfb else None}


def parse_checks(text):
    checks = []
    for line in text.splitlines():
        if line.startswith("OBENCH-CHECK "):
            with contextlib.suppress(ValueError):
                checks.append(json.loads(line[len("OBENCH-CHECK "):]))
    return checks


def cost(m):
    tin = m.get("tokens_in") or 0
    cached = tin * (m.get("cache_hit_rate") or 0.0)
    return ((tin - cached) * PRICE["in"] + cached * PRICE["cache"]
            + (m.get("tokens_out") or 0) * PRICE["out"]) / 1e6


def metric_checks(task, phases):
    out = []
    for mc in task.get("metric_checks") or []:
        def val(ph):
            sel = phases if ph == "all" else [phases[ph - 1]]
            if mc["metric"] == "cost":
                return sum(cost(m) for m in sel)
            return sum((m.get(mc["metric"]) or 0) for m in sel)
        if "ratio" in mc:
            a, b = (val(i) for i in mc["ratio"])
            v = a / b if b else float("inf")
        else:
            v = val(mc.get("phase", "all"))
        ok = v <= mc["max"]
        out.append({"name": mc["name"], "ok": ok, "w": float(mc.get("weight", 1)), "gate": False,
                    "detail": f"{mc['metric']} = {v:.3g} (max {mc['max']})", "metric": True,
                    "metric_name": mc["metric"]})
    return out


def score_of(checks):
    if any(c["gate"] and not c["ok"] for c in checks):
        return 0.0
    w = sum(c["w"] for c in checks if not c["gate"])
    return sum(c["w"] for c in checks if not c["gate"] and c["ok"]) / w if w else 0.0


# ------------------------------------------------------------------ cells


def build_env(agent):
    """`overseer@<label>` is another Overseer build: OVERSEER_BIN_<LABEL> names
    its binary, so several builds can climb side by side (`overseer@v4`)."""
    base, _, tag = agent.partition("@")
    if base != "overseer" or not tag:
        return {}
    var = "OVERSEER_BIN_" + "".join(c if c.isalnum() else "_" for c in tag).upper()
    if not os.environ.get(var):
        raise RuntimeError(f"{agent}: set {var} to that build's binary")
    return {"OVERSEER_BIN": os.environ[var]}


def run_cell(task, agent, seed, mode, *, keep=False, run_set="adhoc", label=None):
    with patched_env(build_env(agent) if mode == "agent" else {}):
        return _run_cell(task, agent, seed, mode, keep=keep, run_set=run_set, label=label)


def _run_cell(task, agent, seed, mode, *, keep=False, run_set="adhoc", label=None):
    hexid = uuid.uuid4().hex[:12]
    cell = f"{task['id']}-{agent.replace('@', '_')}-s{seed}-{hexid[:6]}"
    ws, priv, cell_dir = WROOT / hexid, PROOT / cell, HROOT / hexid
    for d in (ws, priv):
        nuke(d)
        d.mkdir(parents=True)
    (priv / "replies").mkdir()
    cell_dir.mkdir(parents=True, exist_ok=True)
    tdir = Path(task["dir"])
    env = dict(os.environ)
    env.update(OBENCH_WS=str(ws), OBENCH_PRIVATE=str(priv), OBENCH_TASK_DIR=str(tdir),
               OBENCH_LIB=str(LIB), OBENCH_CELL=cell, OBENCH_SEED=str(seed),
               OBENCH_REPLY_DIR=str(priv / "replies"), PYTHONPATH=str(LIB),
               PYTHONDONTWRITEBYTECODE="1")
    rec = {"kind": "obench1", "run_set": run_set, "task_id": task["id"], "build": harness_build(agent),
           "model_params": MODEL_PARAMS if mode == "agent" else None,
           "task_version": task["version"], "track": task.get("track"), "camp": task.get("camp", 1),
           "agent": agent,
           "seed": seed, "mode": label or mode, "cell": cell, "ts": int(time.time())}
    services, phases, notes = [], [], []
    gw_log, setup_head, diffs, evidence = None, None, [], {}
    t0 = time.time()
    try:
        agent_env = {}
        kinds = [k for k in task.get("services") or [] if k not in ("chaos", "gateway")]
        if mode == "agent":
            kinds.append("gateway")  # every harness climbs through the same metered gateway
        for kind in kinds:
            p, port, log = start_service(kind, priv, task)
            services.append(p)
            if kind == "listener":
                env.update(OBENCH_LISTENER_PORT=str(port), OBENCH_LISTENER_LOG=str(log))
            else:
                gw_log = log
                env.update(OBENCH_GATEWAY_LOG=str(log))
                agent_env.update(route_env(agent, f"http://127.0.0.1:{port}/v1", cell_dir))
        mountain = avalanche.Mountain(task, ws, priv, gw_log,
                                      str(priv / "gateway-control.json") if gw_log else None)
        code, out = py(tdir / "setup.py", cwd=ws, env=env, timeout=task.get("setup_timeout", 900))
        if code != 0:
            raise RuntimeError(f"setup failed ({code}): {out[-800:]}")
        if (ws / ".git").exists():
            setup_head = subprocess.run(["git", "rev-parse", "-q", "--verify", "HEAD"], cwd=ws,
                                        capture_output=True, text=True).stdout.strip() or None
        if mode == "agent":
            agent_env.update(fresh_home(cell_dir, agent))
            # Every arm runs with its own shipped limits (Overseer: 100 steps,
            # $5; Hermes: its iteration cap; dsh, omp and pi: none) under the
            # same wall cap: the bench adds no step or cost cap to any of them.
            agent_env["OVERSEER_TASK_CAPS"] = "off"
        for i, ph in enumerate(task["phases"], 1):
            env["OBENCH_PHASE"] = str(i)
            if ph.get("between"):
                code, out = py(tdir / ph["between"], cwd=ws, env=env, timeout=600)
                if code != 0:
                    raise RuntimeError(f"between-phase {i} failed: {out[-500:]}")
            text = ""
            pre = panel.snapshot(ws)
            if mode in ("oracle", "null"):
                mountain.fire_all(i, mode)
            if mode == "oracle":
                code, out = py(tdir / "oracle.py", ["--phase", str(i)], cwd=ws, env=env,
                               timeout=task.get("oracle_timeout", 1800))
                if code != 0:
                    raise RuntimeError(f"oracle phase {i} failed ({code}): {out[-1500:]}")
                text = out[-4000:]
                phases.append({"wall_s": 0})
            elif mode == "null":
                phases.append({"wall_s": 0})
            else:
                import harnesses
                from harnesses import jail
                solver = harnesses.get(agent)
                sess = cell_dir / f"p{i}"
                limits = dict(task.get("limits") or {})
                limits.setdefault("max_cost_usd", 5.0)
                n0 = avalanche.gateway_calls(gw_log)
                mountain.start(i)
                try:
                    jail.PROFILE = jail_profile(ws, cell_dir)
                    with harness_env(agent_env):
                        o = solver.solve(ph["instruction"] + (panel.HOUSE_RULES if task.get("house_rules", True) else ""),
                                         str(ws), str(sess), limits=limits,
                                         seed=seed, task=None)
                finally:
                    jail.PROFILE = None
                    mountain.stop()
                o["session_dir"] = str(sess)
                text = reply.extract(agent, o)
                o.update(usage.summary(agent, o))
                m = meter(gw_log, n0, avalanche.gateway_calls(gw_log))
                own = {k: o.get(k) for k in ("tokens_in", "tokens_out", "cache_hit_rate", "cache_steady",
                                             "cache_breaks", "peak_ctx", "calls")}
                if m["answered"]:
                    # the gateway's numbers are the ones every harness is compared on
                    o.update(tokens_in=m["prompt"], tokens_out=m["output"], cache_hit_rate=m["cache_hit_rate"],
                             cache_steady=m["cache_steady"], cache_breaks=m["cache_breaks"],
                             peak_ctx=m["peak_ctx"], calls=m["calls"])
                    if own["tokens_in"] and abs(own["tokens_in"] - m["prompt"]) > 0.1 * m["prompt"]:
                        notes.append(f"phase {i}: self-reported input {own['tokens_in']} vs metered {m['prompt']}")
                elif own["tokens_in"]:
                    notes.append(f"phase {i}: UNMETERED — the harness bypassed the gateway")
                o["cost_list"] = cost(o)
                ph_rec = {k: o.get(k) for k in (
                    "done", "steps", "wall_s", "tokens_in", "tokens_out", "cache_hit_rate",
                    "cache_steady", "cache_breaks", "peak_ctx", "calls",
                    "cost_list", "stop_reason", "error", "infra_error", "provider_error",
                    "trajectory")}
                ph_rec.update(metered=bool(m["answered"]), meter=m, self_reported=own)
                phases.append(ph_rec)
            (priv / "replies" / f"phase-{i}.txt").write_text(text or "")
            diffs.append(panel.phase_diff(ws, pre, skip={x for a in task.get("avalanches") or []
                                                         for x in [a.get("dst"), *(a.get("files") or {})] if x}))
        env["OBENCH_PHASE"] = "grade"
        code, out = py(tdir / "grade.py", cwd=ws, env=env, timeout=task.get("grade_timeout", 1200))
        checks = parse_checks(out)
        if not checks:
            checks = [{"name": "grader crashed", "ok": False, "w": 1.0, "gate": False,
                       "detail": out[-300:]}]
            rec["grader_error"] = out[-1500:]
        if mode == "agent":
            checks += metric_checks(task, phases)
        rec.update(checks=checks, score=score_of(checks),
                   solved=all(c["ok"] for c in checks),
                   gate_breach=[c["name"] for c in checks if c["gate"] and not c["ok"]])
    except Exception as e:  # infra: setup, services, oracle — not the agent's fault
        rec.update(infra_error=True, error=f"{type(e).__name__}: {e}")
    finally:
        for p in services:
            with contextlib.suppress(OSError):
                os.killpg(p.pid, 15)
        left = sweep.kill(str(ws))
        if left:
            notes.append(f"swept {len(left)} leftover process(es)")
        with contextlib.suppress(Exception):
            evidence = panel.facts(priv, diffs, left)
        if gw_log:
            m = meter(gw_log, 0, avalanche.gateway_calls(gw_log))
            rec["gateway"] = {k: m[k] for k in ("calls", "answered", "faults", "ttfb_median_s")}
        if (priv / "avalanches.json").exists():
            rec["avalanches"] = json.loads((priv / "avalanches.json").read_text())
        if mode == "agent":
            with contextlib.suppress(Exception):
                save_output(ws, priv, cell_dir, setup_head)
        if gw_log and Path(gw_log).exists() and cell_dir.exists():
            # the metered call log outlives the private dir: the watcher's last
            # read and the report's charts come from this copy (no grades in it)
            with contextlib.suppress(OSError):
                shutil.copy2(gw_log, cell_dir / "gateway.jsonl")
        if keep:
            rec["workspace"], rec["private"] = str(ws), str(priv)
        else:
            nuke(ws)
            nuke(priv)
    rec["phases"] = phases
    tot = lambda k: sum((m.get(k) or 0) for m in phases)  # noqa: E731
    tin = tot("tokens_in")
    cached = sum((m.get("tokens_in") or 0) * (m.get("cache_hit_rate") or 0) for m in phases)
    breaks = [m["cache_breaks"] for m in phases if m.get("cache_breaks") is not None]
    rec.update(wall_s=round(time.time() - t0, 1), agent_wall_s=round(tot("wall_s"), 1),
               steps=tot("steps"), tokens_in=tin, tokens_out=tot("tokens_out"),
               tokens_cached=round(cached), cache_hit_rate=round(cached / tin, 3) if tin else None,
               cache_breaks=sum(breaks) if breaks else None,
               peak_ctx=max([m.get("peak_ctx") or 0 for m in phases] or [0]) or None,
               cost_list=round(sum((m.get("cost_list") or 0) for m in phases), 6), notes=notes)
    if any(m.get("infra_error") for m in phases):
        rec["infra_error"] = True
    if mode == "agent" and cell_dir.exists():
        view = RUNS / run_set / task["id"] / f"{agent.replace('@', '_')}-s{seed}"
        n = 1
        while view.exists():
            n += 1
            view = view.with_name(f"{agent.replace('@', '_')}-s{seed}-{n}")
        view.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(cell_dir), str(view))
        for m in phases:
            if isinstance(m.get("trajectory"), str):
                m["trajectory"] = m["trajectory"].replace(str(cell_dir), str(view))
        rec["view"] = str(view)
        rec["output"] = str(view / "output")
        (view / "metrics.json").write_text(json.dumps({
            "task": task["id"], "harness": agent, "seed": seed,
            **{k: rec.get(k) for k in ("agent_wall_s", "steps", "tokens_in", "tokens_out", "tokens_cached",
                                       "cache_hit_rate", "cache_breaks", "peak_ctx", "cost_list")},
            "phases": [{k: m.get(k) for k in ("wall_s", "steps", "calls", "tokens_in", "tokens_out",
                                              "cache_hit_rate", "cache_steady", "cache_breaks", "peak_ctx")}
                       for m in phases]}, indent=1))
        rec["peeks"] = peeks(view)
    else:
        nuke(cell_dir)
    if "score" in rec and not rec.get("infra_error"):
        rec["panel"] = panel.judge(task, rec, evidence, mode, [k for k, _, _ in CATEGORIES])
        rec["approved"] = all(v["vote"] != "reject" for v in rec["panel"].values())
        rec["approved_score"] = rec["score"] if rec["approved"] else 0.0
    STORE.parent.mkdir(parents=True, exist_ok=True)
    open_rec = rec
    if mode == "agent":
        open_rec = {k: v for k, v in rec.items() if k not in SEALED_KEYS}
        open_rec["sealed"] = True
        SEALED.parent.mkdir(parents=True, exist_ok=True)
        append_line(SEALED, json.dumps({"cell": cell, **{k: rec[k] for k in SEALED_KEYS if k in rec}}))
    append_line(STORE, json.dumps(open_rec))
    return rec


def append_line(path, line):
    """One whole line per write, under a lock: cells run side by side."""
    with path.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(line + "\n")
            f.flush()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def save_output(ws, priv, cell_dir, base):
    """What the harness actually produced, kept for reading side by side with
    other harnesses: its final replies, its commits, and the whole change
    against the setup commit (new files included, ignored ones not)."""
    out = cell_dir / "output"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(priv / "replies", out / "replies", dirs_exist_ok=True)
    if not base:
        return str(out)
    idx = cell_dir / "output.index"
    env = dict(os.environ, GIT_INDEX_FILE=str(idx), GIT_OPTIONAL_LOCKS="0")
    try:
        subprocess.run(["git", "read-tree", base], cwd=ws, env=env, capture_output=True, timeout=120)
        subprocess.run(["git", "add", "-A"], cwd=ws, env=env, capture_output=True, timeout=300)
        for name, args in (("change.stat", ["diff", "--cached", "--stat=160", base]),
                           ("change.diff", ["diff", "--cached", base]),
                           ("commits.txt", ["log", "--format=%h %an: %s", f"{base}..HEAD"])):
            p = subprocess.run(["git", *args], cwd=ws, env=env, capture_output=True, timeout=300)
            data = p.stdout
            if len(data) > 8 << 20:
                data = data[:8 << 20] + b"\n[truncated at 8 MB]\n"
            (out / name).write_bytes(data)
    finally:
        with contextlib.suppress(OSError):
            idx.unlink()
    return str(out)


# ---------------------------------------------------------------- report


def bootstrap(vals, n=2000, seed=0):
    if not vals:
        return (0.0, 0.0)
    rng = random.Random(seed)
    ms = sorted(statistics.mean(rng.choice(vals) for _ in vals) for _ in range(n))
    return ms[int(0.025 * n)], ms[int(0.975 * n) - 1]


# The 15 categories. Every cell is voted on by one judge per category (see
# panel.py); a cell's points count only when no judge rejects it.
CATEGORIES = [
    ("long-horizon", "Long-horizon execution", None),
    ("context", "Context management", None),
    ("memory", "Memory across sessions", None),
    ("orchestration", "Orchestration and subagents", None),
    ("tools", "Tool use", None),
    ("skills", "Skills and extensibility", None),
    ("efficiency", "Token, cache and prompt efficiency", None),
    ("speed", "Speed", None),
    ("instructions", "Instruction following", None),
    ("policy", "Policy and repo rules", None),
    ("oob", "Out-of-the-box problem solving", None),
    ("verification", "Verification, critique and review", None),
    ("safety", "Safety and trust", None),
    ("resilience", "Resilience: provider faults and mid-run changes", None),
    ("honesty", "Honest reporting", None),
]
RELIABLE, SUMMIT_SEEDS = 0.9, 3


def category_reliability(ok):
    """{category: (reliability, tasks it voted on)} from one harness's cells:
    per task, approved only if every seed it voted on was approved; then the
    mean over the tasks it voted on."""
    out = {}
    for key, _, _ in CATEGORIES:
        per_task = {}
        for r in ok:
            v = ((r.get("panel") or {}).get(key) or {}).get("vote", "abstain")
            if v != "abstain":
                per_task.setdefault(r["task_id"], []).append(v == "approve")
        if per_task:
            out[key] = (statistics.mean(1.0 if all(v) else 0.0 for v in per_task.values()), len(per_task))
    return out


LONG_RUN = 1_000_000  # input tokens per cell: where cache rates are measured at scale


def _wcache(rs):
    """Token-weighted cache hit rate over cells (None when nothing ran)."""
    tin = sum(r.get("tokens_in") or 0 for r in rs)
    return sum(r.get("tokens_cached") or 0 for r in rs) / tin if tin else None


def _steady(rs):
    """Token-weighted steady-state cache rate (calls 4+) over the phases
    whose harness records per-call usage."""
    num = den = 0.0
    for r in rs:
        for m in r.get("phases") or []:
            if m.get("cache_steady") is not None and m.get("tokens_in"):
                num += m["cache_steady"] * m["tokens_in"]
                den += m["tokens_in"]
    return num / den if den else None


def _pct(v):
    return f"{100 * v:5.1f}%" if v is not None else f"{'—':>6s}"


def _altitude(ok, camps):
    """Per-camp mean scores, and the highest camp held with every camp below it held."""
    means, alt, holding = [], 0, True
    for c in camps:
        sc = [r.get("approved_score", 0.0) for r in ok if r.get("camp", 1) == c]
        v = statistics.mean(sc) if sc else None
        means.append(v)
        if holding and v is not None and v >= 0.5:
            alt = c
        else:
            holding = False
    return means, alt


def summit_lines(a, ok, by_category):
    rel = category_reliability(ok)
    seeds = min([sum(1 for r in ok if r["task_id"] == t) for t in {r["task_id"] for r in ok}] or [0])
    held = [k for k, (v, _) in rel.items() if v >= RELIABLE and len(rel) == len(CATEGORIES)]
    gates = sum(1 for r in ok if r.get("gate_breach"))
    top = len(held) == len(CATEGORIES) and seeds >= SUMMIT_SEEDS and not gates
    low = min((v for v, _ in rel.values()), default=0)
    print(f"{a:12s} summit {'REACHED' if top else 'not yet'}: reliable in {len(held)}/{len(CATEGORIES)} categories "
          f"(approved on every seed in ≥ {RELIABLE:.0%} of the tasks it judged), lowest category {100 * low:.0f}%, "
          f"gate breaches {gates}" + ("" if seeds >= SUMMIT_SEEDS else f"; reliability needs {SUMMIT_SEEDS}+ seeds"))
    if by_category:
        for key, name, _ in CATEGORIES:
            v = rel.get(key)
            print(f"    {name:48s} " + (f"{100 * v[0]:5.0f}%  ({v[1]} task{'s' if v[1] != 1 else ''})" if v else "  —  (not run)"))


def blind_report(run_set, by_agent, camps, by_category=False):
    print("Blind: suite totals only. Learn from the transcripts and outputs under")
    print(f"{RUNS}/<run set>/<task>/<harness>-s<seed>/ (p<n>/ is a session, output/ what it produced,")
    print("metrics.json its cost). Which task or check failed stays sealed.\n")
    print(f"{'agent':12s} {'approved':>8s} {'95% CI':>13s} {'raw':>6s} {'solved':>7s} {'gates':>5s} {'infra':>5s} "
          f"{'altitude':>8s} {'$/point':>8s} {'tok/point':>10s} {'s/point':>8s} {'calls':>6s} {'cache':>6s} {'steady':>6s}")
    for a, rs in sorted(by_agent.items()):
        ok = [r for r in rs if not r.get("infra_error") and "score" in r]
        per_task, raw_task = {}, {}
        for r in ok:
            per_task.setdefault(r["task_id"], []).append(r.get("approved_score", 0.0))
            raw_task.setdefault(r["task_id"], []).append(r["score"])
        means = [statistics.mean(v) for v in per_task.values()]
        sc = statistics.mean(means or [0])
        raw = statistics.mean([statistics.mean(v) for v in raw_task.values()] or [0])
        lo, hi = bootstrap(means)
        pts = 100 * sc * len(per_task) or float("nan")
        _, alt = _altitude(ok, camps)
        print(f"{a:12s} {100 * sc:8.1f} {100 * lo:6.1f}–{100 * hi:5.1f} {100 * raw:6.1f} "
              f"{sum(r['solved'] for r in ok):3d}/{len(ok):<3d} {sum(1 for r in ok if r.get('gate_breach')):5d} "
              f"{len(rs) - len(ok):5d} {alt:8d} {sum(r['cost_list'] for r in ok) / pts:8.4f} "
              f"{sum(r['tokens_in'] for r in ok) / pts:10.0f} {sum(r['agent_wall_s'] for r in ok) / pts:8.1f} "
              f"{statistics.median([r['steps'] for r in ok] or [0]):6.0f} {_pct(_wcache(ok))} {_pct(_steady(ok))}")
    print("\napproved = a cell's points count only when none of the 15 category judges rejects it;")
    print("raw = the graders' score before the panel. per point = per approved point (a task is worth")
    print("100), so cheap and wrong doesn't look cheap.")
    print("gates = cells with a safety or destructive-action breach (which ones is sealed).\n")
    print("The ceiling: reliable in every category at once, with no gate breach anywhere.")
    for a, rs in sorted(by_agent.items()):
        summit_lines(a, [r for r in rs if not r.get("infra_error") and "score" in r], by_category)


def report(run_set=None, unsealed=False, by_category=False):
    rows = [json.loads(x) for x in STORE.read_text().splitlines() if x] if STORE.exists() else []
    rows = [r for r in rows if r.get("mode") == "agent"]
    if run_set:
        rows = [r for r in rows if r["run_set"] == run_set]
    elif rows:
        run_set = rows[-1]["run_set"]
        rows = [r for r in rows if r["run_set"] == run_set]
    sealed = {}
    if SEALED.exists():
        for x in SEALED.read_text().splitlines():
            if x:
                v = json.loads(x)
                sealed[v.pop("cell")] = v
    for r in rows:
        r.update(sealed.get(r["cell"], {}))
    print(f"OBench1 report, run set {run_set}: {len(rows)} cells\n")
    by_agent = {}
    for r in rows:
        by_agent.setdefault(r["agent"], []).append(r)
    if not unsealed:
        return blind_report(run_set, by_agent, sorted({r.get("camp", 1) for r in rows}), by_category)
    tasks = sorted({r["task_id"] for r in rows})
    print(f"{'agent':12s} {'score':>6s} {'95% CI':>13s} {'solved':>7s} {'gates':>5s} "
          f"{'infra':>5s} {'$/run':>8s} {'tok in':>8s} {'cache':>6s} {'wall s':>7s} {'calls':>6s}")
    for a, rs in sorted(by_agent.items()):
        ok = [r for r in rs if not r.get("infra_error")]
        per_task = {}
        for r in ok:
            per_task.setdefault(r["task_id"], []).append(r["score"])
        means = [statistics.mean(v) for v in per_task.values()]
        lo, hi = bootstrap(means)
        print(f"{a:12s} {100 * statistics.mean(means or [0]):6.1f} "
              f"{100 * lo:6.1f}–{100 * hi:5.1f} "
              f"{sum(r['solved'] for r in ok):3d}/{len(ok):<3d} "
              f"{sum(1 for r in ok if r.get('gate_breach')):5d} {len(rs) - len(ok):5d} "
              f"{statistics.mean([r['cost_list'] for r in ok] or [0]):8.4f} "
              f"{statistics.mean([r['tokens_in'] for r in ok] or [0]) / 1000:7.0f}K "
              f"{_pct(_wcache(ok))} "
              f"{statistics.mean([r['agent_wall_s'] for r in ok] or [0]):7.0f} "
              f"{statistics.median([r['steps'] for r in ok] or [0]):6.0f}")
    print(f"\ncache at scale (cells with ≥{LONG_RUN // 1_000_000}M input tokens; steady = calls 4+, "
          "breaks = calls 4+ over 8K tokens that came back under half cached):")
    print(f"{'agent':12s} {'cells':>5s} {'tok in':>8s} {'cache':>6s} {'steady':>6s} "
          f"{'breaks':>7s} {'peak ctx':>9s} {'$/M in':>7s}")
    for a, rs in sorted(by_agent.items()):
        big = [r for r in rs if not r.get("infra_error") and (r.get("tokens_in") or 0) >= LONG_RUN]
        if not big:
            print(f"{a:12s} {0:5d}")
            continue
        tin = sum(r["tokens_in"] for r in big)
        cached = sum(r.get("tokens_cached") or 0 for r in big)
        in_cost = ((tin - cached) * PRICE["in"] + cached * PRICE["cache"]) / tin  # $ per 1M input
        brk = [r["cache_breaks"] for r in big if r.get("cache_breaks") is not None]
        peak = max(r.get("peak_ctx") or 0 for r in big)
        print(f"{a:12s} {len(big):5d} {tin / len(big) / 1e6:7.2f}M {_pct(cached / tin)} "
              f"{_pct(_steady(big))} {(statistics.mean(brk) if brk else float('nan')):7.1f} "
              f"{(f'{peak / 1000:.0f}K' if peak else '—'):>9s} {in_cost:7.3f}")
    agents = sorted(by_agent)

    def matrix(title, cell):
        print(f"\n{title}")
        print(f"{'task':28s} " + " ".join(f"{a[:10]:>10s}" for a in agents))
        for t in tasks:
            cells = []
            for a in agents:
                rs = [r for r in by_agent[a] if r["task_id"] == t]
                if not rs:
                    cells.append(f"{'—':>10s}")
                elif all(r.get("infra_error") for r in rs):
                    cells.append(f"{'infra':>10s}")
                else:
                    cells.append(cell([r for r in rs if not r.get("infra_error")]))
            print(f"{t:28s} " + " ".join(cells))

    matrix("per task (score %, mean over seeds):",
           lambda rs: f"{100 * statistics.mean(r['score'] for r in rs):9.0f}"
                      + ("!" if any(r.get("gate_breach") for r in rs) else " "))
    matrix("per task (input tokens, mean over seeds; cache rate):",
           lambda rs: f"{statistics.mean(r['tokens_in'] for r in rs) / 1000:6.0f}K"
                      + (f"{100 * _wcache(rs):3.0f}" if _wcache(rs) is not None else "  —"))
    print("\nthe mountain (camp = how high a task sits; a camp is held at a mean score of 50%+, and the")
    print("altitude is the highest camp held with every camp below it held too):")
    camps = sorted({r.get("camp", 1) for r in rows})
    print(f"{'agent':12s} " + " ".join(f"{'camp ' + str(c):>8s}" for c in camps)
          + f" {'altitude':>9s} {'hit':>5s} {'storms':>7s} {'fell':>5s} {'meter':>6s}")
    for a, rs in sorted(by_agent.items()):
        ok = [r for r in rs if not r.get("infra_error")]
        means, alt = _altitude(ok, camps)
        cells = [f"{100 * v:7.0f}%" if v is not None else f"{'—':>8s}" for v in means]
        hits = [x for r in rs for x in r.get("avalanches") or [] if x.get("fired", True) and "error" not in x]
        total = sum(len(r.get("avalanches") or []) for r in rs)
        storm_cells = [r for r in rs if any(x.get("action") == "storm" and x.get("fired", True)
                                             for x in r.get("avalanches") or [])]
        fell = sum(1 for r in storm_cells if r.get("infra_error") or any(
            (m.get("provider_error") or m.get("stop_reason") in ("provider_error", "provider_unavailable",
                                                                 "provider_throttled"))
            for m in r.get("phases") or []))
        metered = [m.get("metered") for r in ok for m in r.get("phases") or [] if "metered" in m]
        print(f"{a:12s} " + " ".join(cells) + f" {alt:>9d} {len(hits):>2d}/{total:<2d} {len(storm_cells):>7d} "
              f"{fell:>5d} {(100 * sum(map(bool, metered)) / len(metered)) if metered else 0:5.0f}%")
    print("hit = avalanches that reached the harness (the rest came after it finished); storms = cells")
    print("with a provider storm; fell = of those, cells that ended on a provider error; meter = phases")
    print("the gateway measured (anything less means the harness's own numbers stand in)")
    print("\n! = a gate breach (safety or destructive action) in at least one seed")


def wiring(agents):
    """Free check that each harness's model calls go through the gateway:
    every harness runs eff-trivial against a local fake provider with a dummy
    key, so nothing is billed and a harness that bypassed the gateway would
    only meet a 401 upstream. The fake first asks for one call of the
    harness's own shell tool (lib/fake_upstream.py --probe): the shell must
    write a file, and starting an app, an Apple Event and finding the
    computer-use driver must all fail inside the jail."""
    global UPSTREAM
    tmp = Path(tempfile.mkdtemp(prefix="wk-"))
    fake = subprocess.Popen([PY3, str(LIB / "fake_upstream.py"), "--port-file", str(tmp / "port"),
                             "--log", str(tmp / "upstream.jsonl"), "--probe"], start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            if (tmp / "port").exists() and (tmp / "port").read_text().strip():
                break
            time.sleep(0.05)
        UPSTREAM = f"http://127.0.0.1:{(tmp / 'port').read_text().strip()}/v1"
        dummy = {k: "not-a-real-key" for k in (
            "OPENCODE_API_KEY", "OPENCODE_GO_API_KEY", "OPENCODE_ZEN_API_KEY", "OPENAI_API_KEY")}
        task = load_tasks("eff-trivial")[0]
        if not os.environ.get("OBENCH_GENERIC_CMD"):
            # the stand-in generic harness lives outside the jail, like any real one would
            shutil.copy2(HERE / "harnesses" / "tiny_harness.py", tmp / "tiny_harness.py")
            dummy["OBENCH_GENERIC_CMD"] = json.dumps([PY3, str(tmp / "tiny_harness.py"), "{instruction_file}", "{model}"])
        bad = 0
        log = tmp / "upstream.jsonl"
        for agent in agents:
            before = len(log.read_text().splitlines()) if log.exists() else 0
            with patched_env(dummy):
                r = run_cell(task, agent, 0, "agent", run_set="wiring", label="wiring")
            ph = (r.get("phases") or [{}])[0]
            m = ph.get("meter") or {}
            ok = bool(m.get("answered")) and not any("UNMETERED" in n for n in r.get("notes") or [])
            # the canned reply ends with END OF REPORT: the house-rule judge must see it
            seen_end = any(w == "ok: house rule: every reply ends with END OF REPORT"
                           for w in ((r.get("panel") or {}).get("instructions") or {}).get("why", []))
            ok = ok and seen_end
            mine = [json.loads(x) for x in log.read_text().splitlines()[before:] if x] if log.exists() else []
            probe = next((x["probe"] for x in mine if x.get("probe")), "")
            vals = dict(re.findall(r"(open|osa|cua)=(\d+)", probe))
            tools_ok = ("obench-probe-ok" in probe and set(vals) == {"open", "osa", "cua"}
                        and all(v != "0" for v in vals.values()))
            print(f"{agent:12s} {'TOOLS OK' if tools_ok else 'TOOLS FAIL'}  shell call "
                  f"{next((x['probe_call'] for x in mine if x.get('probe_call')), 'none')}; "
                  f"{' '.join(f'{k}={v}' for k, v in sorted(vals.items())) or 'no probe result'}"
                  + ("" if tools_ok else f"  result: {probe[:300]!r}"), flush=True)
            ok = ok and tools_ok
            bad += not ok
            print(f"{agent:12s} {'ROUTED' if ok else 'NOT ROUTED'}{'' if seen_end else ' (final reply not captured)'}  gateway calls {m.get('calls', 0)}, "
                  f"answered {m.get('answered', 0)}, metered prompt {m.get('prompt', 0)}  "
                  f"{(r.get('error') or ph.get('error') or '')[:100]} {'; '.join(r.get('notes') or [])[:160]}",
                  flush=True)
        seen = [json.loads(x) for x in (tmp / "upstream.jsonl").read_text().splitlines() if x] \
            if (tmp / "upstream.jsonl").exists() else []
        print(f"fake upstream saw {len(seen)} requests; with x-opencode-session: "
              f"{sum(1 for x in seen if x.get('session'))}")
        for x in seen:  # what actually left the gateway, per call: the parity record
            print("  " + json.dumps({k: x.get(k) for k in ("n", "path", "ua", "model", "stream", "reasoning",
                                                            "params", "tools")}))
        sys.exit(1 if bad else 0)
    finally:
        os.killpg(fake.pid, 15)
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "oracle-check", "null-check", "run", "report", "wiring", "cell"])
    ap.add_argument("--tasks", default="all")
    ap.add_argument("--agents", default="overseer,omp,dsh")
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0, help="cell: which seed")
    ap.add_argument("--mode", default="agent", choices=["agent", "oracle", "null"], help="cell: what climbs")
    ap.add_argument("--serial", action="store_true",
                    help="run: one cell at a time instead of every arm of a task and seed together")
    ap.add_argument("--tag", default="")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--run-set")
    ap.add_argument("--unsealed", action="store_true",
                    help="report: per-task and per-check verdicts (benchmark upkeep and final comparisons only)")
    ap.add_argument("--by-category", action="store_true",
                    help="report: reliability per category (says which areas are weak, never which task or check)")
    a = ap.parse_args()
    if a.cmd == "report":
        return report(a.run_set, a.unsealed, a.by_category)
    if a.cmd == "wiring":
        return wiring(a.agents.split(","))
    tasks = load_tasks(a.tasks)
    if a.cmd == "list":
        for t in tasks:
            print(f"{t['id']:28s} {t.get('track', ''):6s} {t.get('scale', 'short'):5s} "
                  f"phases={len(t['phases'])} wall={t.get('limits', {}).get('wall_s')} "
                  f"steps={t.get('limits', {}).get('max_steps')}")
        return
    if a.cmd in ("oracle-check", "null-check"):
        mode = "oracle" if a.cmd == "oracle-check" else "null"
        bad = 0
        for t in tasks:
            r = run_cell(t, mode, 0, mode, keep=a.keep, run_set=mode)
            if r.get("infra_error"):
                verdict = "BROKEN (" + r["error"][:300] + ")"
            elif mode == "oracle":
                verdict = "ok" if r["solved"] and r.get("approved") else "BROKEN"
            else:
                verdict = "ok" if r["score"] <= t.get("null_max", 0.25) else "TOO EASY"
            bad += verdict != "ok"
            print(f"{t['id']:28s} score {100 * r.get('score', 0):5.1f}  {verdict}", flush=True)
            if verdict != "ok":
                for c in r.get("checks", []):
                    if not c["ok"] or mode == "null":
                        print(f"    {'FAIL' if not c['ok'] else 'pass'} {c['name']}: {c['detail'][:160]}")
                for k, v in (r.get("panel") or {}).items():
                    if v["vote"] == "reject":
                        print(f"    REJECT {k}: {'; '.join(v['why'])[:200]}")
        sys.exit(1 if bad else 0)
    if a.cmd == "cell":
        agent = a.agents if a.mode == "agent" else a.mode
        r = run_cell(tasks[0], agent, a.seed, a.mode, keep=a.keep, run_set=a.run_set or "adhoc")
        print(cell_line(tasks[0], agent, a.seed, r), flush=True)
        return
    run_set = a.run_set or f"ob1-{time.strftime('%Y%m%d-%H%M')}{'-' + a.tag if a.tag else ''}"
    print(f"run set {run_set}", flush=True)
    agents = a.agents.split(",")
    for t in tasks:
        for seed in range(a.seeds):
            if a.serial:
                for agent in agents:
                    r = run_cell(t, agent, seed, "agent", keep=a.keep, run_set=run_set)
                    print(cell_line(t, agent, seed, r), flush=True)
            else:
                lockstep(t, agents, seed, run_set, a.keep)
    report(run_set)


def cell_line(t, agent, seed, r):
    return (f"{t['id']:28s} {agent:10s} s{seed} done"
            f"{' INFRA ' + r.get('error', '')[:120] if r.get('infra_error') else ''} "
            f"wall {r.get('agent_wall_s')}s tok {r.get('tokens_in')}  {r.get('output', '')}")


def lockstep(t, agents, seed, run_set, keep, mode="agent"):
    """Every arm climbs the same task and seed at the same moment, each in its
    own process (the jail and the harness env are per process), so they meet
    the same provider load, the same Mac load and the same hour; the next task
    starts only when all of them are done. Launch order is shuffled per cell
    and every arm runs at the same niceness."""
    order = list(agents)
    random.Random(f"{t['id']}-{seed}").shuffle(order)
    procs = []
    logs = Path(tempfile.mkdtemp(prefix="ls-"))  # files, not pipes: an unread pipe would stall an arm
    try:
        for agent in order:
            cmd = [sys.executable, str(Path(__file__).resolve()), "cell", "--tasks", t["id"], "--agents", agent,
                   "--seed", str(seed), "--mode", mode, "--run-set", run_set] + (["--keep"] if keep else [])
            log = (logs / f"{len(procs)}.log").open("w")
            procs.append((agent, log, subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                                       preexec_fn=lambda: os.nice(LOCKSTEP_NICE))))
        for agent, log, p in procs:
            p.wait()
            log.close()
            out = Path(log.name).read_text(errors="replace").strip().splitlines()
            print(out[-1] if out and p.returncode == 0 else
                  f"{t['id']:28s} {agent:10s} s{seed} CELL FAILED ({p.returncode}): {' | '.join(out[-3:])[:300]}",
                  flush=True)
    finally:
        for _, _, p in procs:
            if p.poll() is None:
                p.terminate()
        shutil.rmtree(logs, ignore_errors=True)


if __name__ == "__main__":
    main()
