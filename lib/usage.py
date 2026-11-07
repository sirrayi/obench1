"""Per-call prompt usage from what an adapter kept, for cache measurement.

`series` gives (prompt tokens, cached tokens) per model call where the
harness records it per call (overseer, pi, omp); Hermes and mini report
run totals only, so their steady-state numbers stay empty. `summary`
reduces a series to the numbers the report prints:

- cache_steady: cached / prompt over calls 4+ (the first calls pay for
  the prefix on any harness; past them, a miss is the harness's doing)
- cache_breaks: calls 4+ with a prompt over 8K tokens that came back
  under half cached — a rewritten prefix
- peak_ctx: the largest single prompt
"""

import json
from pathlib import Path

WARMUP = 3
BREAK_MIN_PROMPT = 8000


def _jsonl(path):
    out = []
    try:
        for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def _overseer(outcome):
    rows = []
    for e in _jsonl(outcome.get("trajectory") or ""):
        if e.get("type") == "model_response":
            u = e.get("usage") or {}
            total = (u.get("fresh_input") or 0) + (u.get("cache_read") or 0) + (u.get("cache_write") or 0)
            rows.append((total, u.get("cache_read") or 0))
    return rows


def _pi(outcome):
    rows = []
    for e in _jsonl(outcome.get("trajectory") or ""):
        m = e.get("message") or {}
        if e.get("type") == "message_end" and m.get("role") == "assistant":
            u = m.get("usage") or {}
            total = (u.get("input") or 0) + (u.get("cacheRead") or 0) + (u.get("cacheWrite") or 0)
            rows.append((total, u.get("cacheRead") or 0))
    return rows


def series(agent, outcome):
    fn = {"overseer": _overseer, "pi": _pi, "omp": _pi}.get(agent.split("@", 1)[0])
    try:
        return fn(outcome) if fn else None
    except Exception:  # an unreadable trajectory is no series, not a crash
        return None


def summary(agent, outcome):
    rows = series(agent, outcome)
    if not rows:
        return {"calls": None, "cache_steady": None, "cache_breaks": None, "peak_ctx": None}
    tail = rows[WARMUP:]
    t = sum(a for a, _ in tail)
    return {
        "calls": len(rows),
        "cache_steady": round(sum(c for _, c in tail) / t, 3) if t else None,
        "cache_breaks": sum(1 for a, c in tail if a > BREAK_MIN_PROMPT and c < a / 2),
        "peak_ctx": max(a for a, _ in rows),
    }
