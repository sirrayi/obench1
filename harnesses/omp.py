"""omp arm — oh-my-pi (a pi fork), headless, through the pi arm's runner.

`omp -p --mode json` in the task workdir on the same provider and model as
the overseer arm, saving its session as shipped into the cell's throwaway
agent dir. omp emits pi's JSON event stream, so usage,
steps and cost parse exactly as in `pi.py`. omp has no `--offline` or
`--no-approve`; print mode runs tools without asking.

omp reads the same `PI_CODING_AGENT_DIR` variable as pi (default
`~/.omp/agent`), so a run with both arms points omp at its own throwaway
dir through OMP_AGENT_DIR — the owner's `~/.omp` stays untouched.

omp has no step or cost cap: only the wall cap applies.

Env: OMP_BIN (default `omp` on PATH), OMP_AGENT_DIR, OMP_PROVIDER (else
PI_PROVIDER, else OVERSEER_PROVIDER), OVERSEER_MODEL, OMP_THINKING (else
PI_THINKING, default `medium`).
"""

from __future__ import annotations

import os

from . import pi


def _cfg() -> tuple[str, str, str, str]:
    """Resolved per call — module-level env binding would freeze --model."""
    return (
        os.environ.get("OMP_BIN", "omp"),
        os.environ.get("OMP_PROVIDER")
        or os.environ.get("PI_PROVIDER")
        or os.environ.get("OVERSEER_PROVIDER", "opencode"),
        os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash"),
        os.environ.get("OMP_THINKING") or os.environ.get("PI_THINKING", "medium"),
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
    env = dict(os.environ)
    if os.environ.get("OMP_AGENT_DIR"):
        env["PI_CODING_AGENT_DIR"] = os.environ["OMP_AGENT_DIR"]
    flags = [
        "-p",
        "--mode",
        "json",
        "--provider",
        provider,
        "--model",
        model,
        "--thinking",
        thinking,
    ]
    return pi.run(
        binary, flags, instruction, workdir, session_dir,
        model=model, limits=limits, on_start=on_start, env=env,
    )
