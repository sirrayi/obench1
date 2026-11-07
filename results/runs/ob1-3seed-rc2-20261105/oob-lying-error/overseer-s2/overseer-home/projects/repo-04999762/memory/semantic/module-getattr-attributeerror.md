---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e124
added: 2026-11-05
cues: __getattr__, AttributeError, hasattr, import, python
valid_from: 2026-11-05T22:49:38Z
---
A module-level __getattr__ must raise AttributeError, never ValueError or other exceptions, for unknown names. Import machinery calls hasattr(module, '__path__') on every from-import and hasattr only swallows AttributeError, so other exceptions break `from module import name`; this applies to calendar.py.
