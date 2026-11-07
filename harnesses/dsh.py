"""dsh arm — DeepSeek Harness, headless, from the owner's installed app.

The app bundles the dsh CLI and starts it with its own Electron binary in
node mode; this arm does the same (`ELECTRON_RUN_AS_NODE=1
--expose-internals <app>/.../@deepseek-ai/dsh/lib/bin.js`) with the
one-shot profile, `dsh --profile headless "<task>"`, in the task workdir.
dsh prints the turn's final assistant text and exits 0 once the turn
completed; the session's event log is the trajectory. dsh stores it as
appended zstd frames (session.jsonl.zstd); it is decoded with the zstd
CLI, which the arm needs: a transcript the peek scan can't read would
hide a peek.

dsh keeps profiles, settings and sessions under DSH_HOME; the runner gives
every cell a throwaway one (obench.py fresh_home), so the owner's ~/.dsh
and the app's own profile stay untouched. Its native DeepSeek provider
reads DEEPSEEK_BASE_URL (the cell's gateway, route_env) and
DEEPSEEK_API_KEY, which this arm fills from the run's provider key. The
model is the cell home's `agent-default-model` setting.

Permission mode is danger-full-access (approval never), as Overseer runs
with --full-access: a headless run has no one to approve a tool call.
dsh has no step or cost cap: only the wall cap applies. Telemetry stays at
its shipped default, off.

Env: DSH_APP (default /Applications/DeepSeek Harness.app), OVERSEER_MODEL,
DSH_EFFORT (low, high, max or off; default unset, dsh's own default).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from . import jail, keys

DEFAULT_APP = "/Applications/DeepSeek Harness.app"
ENTRY = "Contents/Resources/app/node_modules/@deepseek-ai/dsh/lib/bin.js"


def _cfg() -> tuple[Path, str]:
    """Resolved per call — module-level env binding would freeze --model."""
    return (
        Path(os.environ.get("DSH_APP", DEFAULT_APP)),
        os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash"),
    )


def executable(app: Path) -> Path:
    return app / "Contents" / "MacOS" / app.stem


def version(app: Path | None = None) -> str | None:
    """`app <ver> dsh <ver>`: the desktop wrapper and the CLI it bundles."""
    app = app or _cfg()[0]
    out = []
    for label, p in (("app", app / "Contents/Resources/app/package.json"),
                     ("dsh", (app / ENTRY).parent.parent / "package.json")):
        try:
            out.append(f"{label} {json.loads(p.read_text())['version']}")
        except (OSError, ValueError, KeyError):
            return None
    return " ".join(out)


def zstd() -> str | None:
    return shutil.which("zstd", path="/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", ""))


def settings(home: Path, model: str) -> None:
    """The cell home's settings.yaml: which model the headless run asks for."""
    effort = os.environ.get("DSH_EFFORT")
    lines = ["agent-default-model:", "  provider: deepseek-official", f"  model: {json.dumps(model)}"]
    if effort:
        lines.append(f"  reasoningEffort: {json.dumps(effort)}")
    (home / "settings.yaml").write_text("\n".join(lines) + "\n")


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
    app, model = _cfg()
    unzstd = zstd()
    if not unzstd:
        return {
            "done": False,
            "error": "zstd missing: dsh transcripts would stay compressed",
            "infra_error": True,
            "wall_s": 0.0,
            "model": model,
            "ts": int(time.time()),
        }
    home = Path(os.environ.get("DSH_HOME") or Path(session_dir) / "dsh-home")
    home.mkdir(parents=True, exist_ok=True)
    settings(home, model)
    sess = Path(session_dir)
    sess.mkdir(parents=True, exist_ok=True)
    logs = home / "sessions"
    before = set(logs.rglob("session.jsonl*")) if logs.exists() else set()

    env = dict(os.environ)
    env.update(
        ELECTRON_RUN_AS_NODE="1",
        DSH_HOME=str(home),
        DSH_AGENTS_HOME=str(home / "agents"),  # not the owner's ~/.agents skills
        DSH_PERMISSION_MODE="danger-full-access",
        DSH_TELEMETRY_MODE="DISABLED",
        DEEPSEEK_API_KEY=os.environ.get(keys.key_env(), ""),
    )
    cmd = [str(executable(app)), "--expose-internals", str(app / ENTRY),
           "--profile", "headless", instruction]

    t0 = time.time()
    stop = None
    try:
        proc = subprocess.Popen(
            jail.wrap(cmd),
            cwd=workdir,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stop = on_start(proc.pid) if on_start else None
        try:
            out, err = proc.communicate(timeout=wall_cap)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise
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
            "error": f"app missing: {app}",
            "infra_error": True,
            "wall_s": 0.0,
            "model": model,
            "ts": int(time.time()),
        }
    finally:
        if stop:
            stop()
    wall_s = time.time() - t0

    (sess / "stdout.txt").write_text(out)
    # this run's session logs (subagents' too), decoded next to the cell's other transcripts
    new = sorted(set(logs.rglob("session.jsonl*")) - before) if logs.exists() else []
    events = []
    for i, p in enumerate(new):
        dst = sess / f"dsh-session-{i}.jsonl"
        if p.suffix == ".zstd":
            with open(dst, "wb") as f:
                subprocess.run([unzstd, "-dcq", str(p)], stdout=f, check=False)
        else:
            shutil.copy2(p, dst)
        for line in dst.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                pass
    traj = sess / "trajectory.jsonl"
    traj.write_text("\n".join(json.dumps(e) for e in events))

    errored = "dsh: " in err
    return {
        "done": proc.returncode == 0,
        "provider_error": errored and proc.returncode != 0,
        "error": next((ln for ln in err.splitlines() if ln.startswith("dsh: ")), None),
        "steps": sum(1 for e in events if e.get("type") == "assistant/message"),
        "wall_s": round(wall_s, 1),
        "trajectory": str(traj),
        "exit_code": proc.returncode,
        "stderr": err[-2000:],
        "model": model,
        "ts": int(time.time()),
    }
