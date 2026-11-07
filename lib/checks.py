"""Grader helpers. Graders run as `python3 grade.py` in the workspace with
OBENCH_* env set by the runner, and print one OBENCH-CHECK line per check.
Python 3.9, stdlib only — graders run on the system interpreter.

    from checks import Grader
    g = Grader()
    g.check("tests pass", ok, weight=3)
    g.gate("vendor untouched", ok)   # failing a gate zeroes the task
    g.check("reply names the blocker", ok, cat="honesty")  # the category judge it reports to
    g.done()
"""

import hashlib
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

WS = Path(os.environ.get("OBENCH_WS", "."))
PRIVATE = Path(os.environ.get("OBENCH_PRIVATE", "."))
TASK_DIR = Path(os.environ.get("OBENCH_TASK_DIR", Path(sys.argv[0]).resolve().parent))
REPLY_DIR = Path(os.environ.get("OBENCH_REPLY_DIR", PRIVATE / "replies"))


class Grader:
    def __init__(self):
        self.n = 0

    def _emit(self, name, ok, weight, gate, detail, cat=None):
        self.n += 1
        rec = {"name": name, "ok": bool(ok), "w": float(weight), "gate": gate,
               "detail": str(detail)[:300]}
        if cat:
            rec["cat"] = cat
        print("OBENCH-CHECK " + json.dumps(rec, ensure_ascii=False), flush=True)
        return bool(ok)

    def check(self, name, ok, weight=1.0, detail="", cat=None):
        return self._emit(name, ok, weight, False, detail, cat)

    def gate(self, name, ok, detail="", cat=None):
        return self._emit(name, ok, 0.0, True, detail, cat)

    def done(self):
        if not self.n:
            print("OBENCH-CHECK " + json.dumps({"name": "grader emitted nothing", "ok": False,
                                                "w": 1.0, "gate": False, "detail": ""}))
        sys.exit(0)


def run(cmd, timeout=120, cwd=None, env=None, input=None):
    """Run in its own process group; on timeout the whole group dies, so a
    grandchild holding the pipe can't hang the grader. Returns
    (code, stdout+stderr) with code -9 on timeout."""
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.Popen(cmd, cwd=cwd or WS, env=e, shell=isinstance(cmd, str),
                         stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         start_new_session=True)
    try:
        out, _ = p.communicate(input=input.encode() if isinstance(input, str) else input,
                               timeout=timeout)
        return p.returncode, out.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            out, _ = p.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            out = b""
        return -9, (out or b"").decode("utf-8", "replace")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path, default=None):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return default


def read_bytes(path, default=None):
    try:
        return Path(path).read_bytes()
    except OSError:
        return default


def replies():
    """Final replies by phase, oldest first ('' where none was captured)."""
    out = []
    for p in sorted(REPLY_DIR.glob("phase-*.txt")):
        out.append(p.read_text(encoding="utf-8", errors="replace"))
    return out


def git(*args, cwd=None):
    code, out = run(["git", *args], cwd=cwd or WS, timeout=60)
    return code, out


def tree_digest(root, exclude=()):
    """{relative path: sha256} of regular files under root (symlinks not
    followed), skipping any path whose first part is in `exclude`."""
    root = Path(root)
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        if rel_dir.parts and rel_dir.parts[0] in exclude:
            dirnames[:] = []
            continue
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.is_symlink() or not p.is_file():
                continue
            out[str(p.relative_to(root))] = sha256(p)
    return out


def load_private(name, default=None):
    p = PRIVATE / name
    if not p.exists():
        return default
    return json.loads(p.read_text())


def save_private(name, obj):
    PRIVATE.mkdir(parents=True, exist_ok=True)
    (PRIVATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True))


def leftover_processes(marker):
    """Processes (other than this grader) whose cwd or command line sits
    in `marker` (the workspace path)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sweep
    me = {os.getpid(), os.getppid()}
    return [p for p in sweep.find(str(marker)) if p[0] not in me]
