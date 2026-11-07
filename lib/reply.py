"""The final reply a harness gave, from what its adapter kept. Graders read
it (OBENCH_REPLY_DIR/phase-N.txt) to catch claims the workspace disproves
and secrets the reply leaks."""

import json
from pathlib import Path


def _jsonl(path):
    out = []
    try:
        for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def overseer(outcome):
    last = ""
    for e in _jsonl(outcome.get("trajectory") or ""):
        if e.get("type") == "model_response":
            text = "".join(b.get("text", "") for b in e.get("blocks", []) if b.get("type") == "text")
            if text.strip():
                last = text
    return last


def pi(outcome):
    last = ""
    for e in _jsonl(outcome.get("trajectory") or ""):
        m = e.get("message") or {}
        if e.get("type") == "message_end" and m.get("role") == "assistant":
            parts = m.get("content") or []
            text = "".join(c.get("text", "") for c in parts if isinstance(c, dict) and c.get("type") == "text")
            if text.strip():
                last = text
    return last


def hermes(outcome):
    p = Path(outcome.get("session_dir") or "") / "stdout.txt"
    try:
        return p.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return ""


def mini(outcome):
    try:
        traj = json.loads(Path(outcome.get("trajectory") or "").read_text())
    except (OSError, ValueError):
        return ""
    for step in reversed(traj):
        if step.get("reply"):
            return step["reply"]
    return ""


def extract(agent, outcome):
    base = agent.split("@", 1)[0]
    fn = _FNS.get(base)
    try:
        return fn(outcome) if fn else ""
    except Exception:  # a reply we can't read is an empty reply, not a crash
        return ""


def generic(outcome):
    try:
        return Path(outcome.get("trajectory") or "").read_text(encoding="utf-8", errors="replace").strip()[-20000:]
    except OSError:
        return ""


_FNS = {"overseer": overseer, "pi": pi, "omp": pi, "hermes": hermes, "dsh": hermes, "mini": mini, "generic": generic}
