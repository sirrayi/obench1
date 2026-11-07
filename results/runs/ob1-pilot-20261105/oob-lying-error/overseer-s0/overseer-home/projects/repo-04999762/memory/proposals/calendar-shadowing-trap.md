---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e167
added: 2026-11-05
layer: semantic
cues: calendar, import-error, module-shadowing
---
The repo has a top-level calendar.py that shadows the stdlib calendar module. A module-level __getattr__ that raises ValueError for any missing attribute breaks importlib's hasattr(module, "__path__") probe during `from calendar import ...`, surfacing as a misleading domain error (e.g. "invalid date header"). Never let __getattr__ raise for unknown attributes there.
