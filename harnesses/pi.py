"""pi arm — the pi coding agent (earendil-works/pi-coding-agent), headless.

`pi -p --mode json` in the task workdir with no project-local pi config
trusted (AGENTS.md still loads), saving its session as shipped into the
cell's throwaway agent dir, on the same provider and model as the
overseer arm (OVERSEER_PROVIDER / OVERSEER_MODEL), so a paired delta reads
scaffold vs scaffold. The JSONL event stream is the trajectory; usage and
cost come from each assistant `message_end` (pi's own price catalog). The
solver never grades.

pi has no step or cost cap: only the wall cap applies, and `steps` is
counted afterwards (one per assistant message).

Env: PI_BIN (default `pi` on PATH), OVERSEER_PROVIDER, OVERSEER_MODEL,
PI_PROVIDER (pi's name for the provider when it differs — a custom
`models.json` provider under PI_CODING_AGENT_DIR), PI_THINKING (default
`medium`, Overseer's default effort); pi resolves the key itself (the
provider's key variable, or the custom provider's `apiKey`).
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

from . import jail


def _cfg() -> tuple[str, str, str, str]:
    """Resolved per call — module-level env binding would freeze --model."""
    return (
        os.environ.get("PI_BIN", "pi"),
        os.environ.get("PI_PROVIDER") or os.environ.get("OVERSEER_PROVIDER", "opencode"),
        os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash"),
        os.environ.get("PI_THINKING", "medium"),
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
    binary, provider, model, thinking = _cfg()
    flags = [
        "-p",
        "--mode",
        "json",
        "--no-approve",
        "--offline",
        "--provider",
        provider,
        "--model",
        model,
        "--thinking",
        thinking,
    ]
    return run(
        binary, flags, instruction, workdir, session_dir,
        model=model, limits=limits, on_start=on_start,
    )


def run(
    binary: str,
    flags: list[str],
    instruction: str,
    workdir: str,
    session_dir: str,
    *,
    model: str,
    limits: dict | None = None,
    on_start=None,
    env: dict | None = None,
) -> dict:
    """One headless run of a pi-family CLI (pi, omp): `binary flags --
    instruction` in the workdir, parsed from pi's JSON event stream."""
    limits = limits or {}
    wall_cap = int(limits.get("wall_s", 900))
    Path(session_dir).mkdir(parents=True, exist_ok=True)
    cmd = [binary, *flags, "--", instruction]

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

    events = []
    for line in proc.stdout.split("\n"):  # strict LF framing (pi json.md)
        if line.strip():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    traj = Path(session_dir) / "trajectory.jsonl"
    traj.write_text("\n".join(json.dumps(e) for e in events))

    replies = [
        e["message"]
        for e in events
        if e.get("type") == "message_end"
        and (e.get("message") or {}).get("role") == "assistant"
    ]

    def _u(m, key):
        return (m.get("usage") or {}).get(key, 0) or 0

    total_in = sum(_u(m, "input") + _u(m, "cacheRead") + _u(m, "cacheWrite") for m in replies)
    cache_read = sum(_u(m, "cacheRead") for m in replies)
    last = replies[-1] if replies else {}
    settled = next((e for e in reversed(events) if e.get("type") == "agent_settled"), {})
    errored = last.get("stopReason") == "error"

    return {
        "done": proc.returncode == 0
        and bool(replies)
        and not errored
        and not settled.get("aborted", False),
        "stop_reason": last.get("stopReason"),
        "provider_error": errored,
        "error": last.get("errorMessage"),
        "steps": len(replies),
        "wall_s": round(wall_s, 1),
        "tokens_in": total_in,
        "tokens_out": sum(_u(m, "output") for m in replies),
        "cache_hit_rate": round(cache_read / total_in, 3) if total_in else 0.0,
        "cost_usd": sum(((m.get("usage") or {}).get("cost") or {}).get("total", 0.0) for m in replies),
        "trajectory": str(traj),
        "exit_code": proc.returncode,
        "stderr": proc.stderr[-2000:],
        "model": model,
        "ts": int(time.time()),
    }
