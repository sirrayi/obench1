---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e106
added: 2026-11-05
layer: semantic
cues: imports, module-layout, stdlib
---
Never put helper modules at repo root whose names collide with stdlib modules (e.g. calendar.py); they shadow the stdlib for every import in the project. Keep such helpers inside the package and import them relatively, e.g. `from .calendar import billing_days`.
