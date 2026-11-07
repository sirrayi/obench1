"""Generic arm: any CLI harness, driven by a command template.

`OBENCH_GENERIC_CMD` is the command as a JSON list (run without a shell),
with placeholders {instruction}, {instruction_file}, {workdir},
{session_dir}, {base_url} and {model}. The harness must send its model
calls to {base_url} — the cell gateway, also exported as
OPENAI_BASE_URL and OPENAI_API_BASE — because that is
where its tokens, cache hits and faults are measured: nothing is read
from the harness itself. stdout is its final reply.

    OBENCH_GENERIC_CMD='["myagent", "--cwd", "{workdir}", "--prompt-file", "{instruction_file}"]'

A second one runs as `generic@<label>` with OBENCH_GENERIC_CMD_<LABEL>.
The wall cap applies; step and cost caps are the harness's own business.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

from . import jail


def _template(label: str | None) -> list[str]:
    key = "OBENCH_GENERIC_CMD" + (f"_{label.upper().replace('-', '_')}" if label else "")
    raw = os.environ.get(key)
    if not raw:
        raise KeyError(f"{key} is not set")
    cmd = json.loads(raw)
    if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) for x in cmd):
        raise ValueError(f"{key} must be a JSON list of strings")
    return cmd


class Generic:
    def __init__(self, label: str | None = None):
        # read now: the runner strips OBENCH_* from the environment before the harness starts
        self.label = label
        try:
            self.tmpl, self.err = _template(label), None
        except (KeyError, ValueError) as e:
            self.tmpl, self.err = None, e

    def solve(self, instruction, workdir, session_dir, *, limits=None, seed=0, task=None, on_start=None):
        limits = limits or {}
        wall_cap = int(limits.get("wall_s", 900))
        sess = Path(session_dir)
        sess.mkdir(parents=True, exist_ok=True)
        model = os.environ.get("OVERSEER_MODEL", "deepseek-v4.1-flash")
        base_url = os.environ.get("OPENAI_BASE_URL", "")
        ifile = sess / "instruction.txt"
        ifile.write_text(instruction)
        tmpl = self.tmpl
        if tmpl is None:
            e = self.err
            return {"done": False, "error": str(e), "infra_error": True, "wall_s": 0.0, "model": model,
                    "ts": int(time.time())}
        subs = {"instruction": instruction, "instruction_file": str(ifile), "workdir": workdir,
                "session_dir": str(sess), "base_url": base_url, "model": model}
        cmd = [x.format(**subs) for x in tmpl]
        env = dict(os.environ)
        if base_url:
            env.update(OPENAI_BASE_URL=base_url, OPENAI_API_BASE=base_url)
        t0 = time.time()
        try:
            proc = subprocess.Popen(jail.wrap(cmd), cwd=workdir, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, env=env, start_new_session=True)
        except FileNotFoundError:
            return {"done": False, "error": f"binary missing: {cmd[0]}", "infra_error": True, "wall_s": 0.0,
                    "model": model, "ts": int(time.time())}
        stop = on_start(proc.pid) if on_start else None
        try:
            out, err = proc.communicate(timeout=wall_cap)
            timed_out = False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            out, err = proc.communicate()
            timed_out = True
        finally:
            if stop:
                stop()
        (sess / "stdout.txt").write_text(out or "")
        (sess / "stderr.txt").write_text(err or "")
        return {"done": proc.returncode == 0 and not timed_out, "infra_error": False,
                "error": f"wall timeout {wall_cap}s" if timed_out else None,
                "wall_s": round(time.time() - t0, 1), "exit_code": proc.returncode,
                "stderr": (err or "")[-2000:], "trajectory": str(sess / "stdout.txt"), "model": model,
                "ts": int(time.time())}
