"""Hermes arm — Nous Hermes Agent, one-shot (`hermes -z`), headless.

`hermes -z <instruction> --yolo --provider <p> -m <model> --usage-file
<json>` in the task workdir, on the same model as the overseer arm. Every
run gets a fresh HERMES_HOME under its session dir: the owner's
`~/.hermes` is never read or written, and Hermes' memory, skills and
session store can't carry one task into the next. Otherwise it runs as
shipped (default toolsets, persona and rules handling).

The usage report gives tokens, api_calls and Hermes' own cost estimate
for the main task (aux calls such as title generation are left out).
Its `input_tokens` is the whole prompt, cache reads included — checked
2026-10-29: the run's `session_model_usage` row held 13,545 uncached +
40,064 cached = the report's 53,609.
The session store under the run's HERMES_HOME is the trajectory. `--yolo`
skips the approval prompts that would otherwise block a headless run.

Hermes keeps its own iteration cap; the rig's wall cap applies on top.

Env: HERMES_BIN (default `hermes` on PATH), HERMES_PROVIDER (default
`opencode-zen`), OVERSEER_MODEL, HERMES_REASONING (unset = Hermes'
default; set to pass `--reasoning`), HERMES_SHARED_DIR (set it for any
matrix run: each home links `installs`/`cache` there instead of
building its own ~600 MB copy). The key is the provider's own
variable — OPENCODE_ZEN_API_KEY / OPENCODE_GO_API_KEY for opencode-zen /
opencode-go, filled from OPENCODE_API_KEY when unset.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

from . import jail


SHARED_SUBDIRS = ("installs", "cache")
# Hermes' own key variable per OpenCode provider, filled from the rig's.
OPENCODE_KEY_VARS = {
    "opencode-zen": "OPENCODE_ZEN_API_KEY",
    "opencode-go": "OPENCODE_GO_API_KEY",
}


def _cfg() -> tuple[str, str, str, str | None]:
    """Resolved per call — module-level env binding would freeze --model."""
    return (
        os.environ.get("HERMES_BIN", "hermes"),
        os.environ.get("HERMES_PROVIDER", "opencode-zen"),
        os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash"),
        os.environ.get("HERMES_REASONING") or None,
    )


def solve(
    instruction: str,
    workdir: str,
    session_dir: str,
    *,
    limits: dict | None = None,
    seed: int = 0,
    task=None,
    on_start=None,
) -> dict:
    limits = limits or {}
    wall_cap = int(limits.get("wall_s", 900))
    binary, provider, model, reasoning = _cfg()
    sess = Path(session_dir)
    sess.mkdir(parents=True, exist_ok=True)
    # OBench1 keeps one home across a cell's phases so memory can carry.
    home = Path(os.environ.get("HERMES_HOME_OVERRIDE") or sess / "hermes-home")
    home.mkdir(parents=True, exist_ok=True)
    shared = os.environ.get("HERMES_SHARED_DIR")
    if shared:
        # A fresh home installs ~350 MB of tool environments and ~250 MB of
        # cache; neither holds memory or sessions, so runs share one copy.
        for sub in SHARED_SUBDIRS:
            target = Path(shared) / sub
            target.mkdir(parents=True, exist_ok=True)
            link = home / sub
            if not link.exists():
                link.symlink_to(target)
    usage_path = sess / "usage.json"

    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)
    key_var = OPENCODE_KEY_VARS.get(provider)
    if key_var and not env.get(key_var):
        env[key_var] = env.get("OPENCODE_API_KEY", "")

    cmd = [
        binary,
        "-z",
        instruction,
        "--yolo",
        "--provider",
        provider,
        "-m",
        model,
        "--usage-file",
        str(usage_path),
        *(["--reasoning", reasoning] if reasoning else []),
    ]

    t0 = time.time()
    stop = None
    try:
        proc = subprocess.Popen(
            jail.wrap(cmd),
            cwd=workdir,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        stop = on_start(proc.pid) if on_start else None
        try:
            out, err = proc.communicate(timeout=wall_cap)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise
        proc = subprocess.CompletedProcess(cmd, proc.returncode, out, err)
    except subprocess.TimeoutExpired:
        return {
            "done": False,
            "error": f"wall timeout {wall_cap}s",
            "infra_error": False,
            "wall_s": wall_cap,
            "model": model,
            "ts": int(time.time()),
        }
    except FileNotFoundError:
        return {
            "done": False,
            "error": f"binary missing: {binary}",
            "infra_error": True,
            "wall_s": 0.0,
            "model": model,
            "ts": int(time.time()),
        }
    finally:
        if stop:
            stop()
    wall_s = time.time() - t0
    (sess / "stdout.txt").write_text(proc.stdout or "")  # the final reply (OBench1)
    return parse(proc, usage_path, home, model, wall_s)


def parse(proc, usage_path: Path, home: Path, model: str, wall_s: float) -> dict:
    """The outcome dict from one finished run's exit code and usage report."""
    try:
        u = json.loads(usage_path.read_text())
    except (OSError, ValueError):
        u = None
    if u is None:
        # No report at all: Hermes never got as far as a turn.
        return {
            "done": False,
            "error": f"no usage report (exit {proc.returncode}): {proc.stderr[-300:]}",
            "infra_error": True,
            "wall_s": round(wall_s, 1),
            "model": model,
            "ts": int(time.time()),
        }

    def n(key):
        return int(u.get(key) or 0)

    total_in = n("input_tokens")
    failure = u.get("failure")
    return {
        "done": proc.returncode == 0 and bool(u.get("completed")),
        "infra_error": False,
        "stop_reason": u.get("turn_exit_reason"),
        "provider_error": bool(failure) and n("api_calls") == 0,
        "error": failure,
        "steps": n("api_calls"),
        "wall_s": round(wall_s, 1),
        "tokens_in": total_in,
        "tokens_out": n("output_tokens"),
        "cache_hit_rate": round(n("cache_read_tokens") / total_in, 3) if total_in else 0.0,
        "cost_usd": float(u.get("estimated_cost_usd") or 0.0),
        "trajectory": str(home),
        "exit_code": proc.returncode,
        "stderr": proc.stderr[-2000:],
        "model": u.get("model") or model,
        "ts": int(time.time()),
    }
