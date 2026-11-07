---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e167
added: 2026-11-05
layer: semantic
cues: proration, rounding, billing
---
billing/proration.py rounds charges half up using exact integer arithmetic; never truncate with int(). Keep the half-cent remainder rather than discarding it.
