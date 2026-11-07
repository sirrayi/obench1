---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e3711
added: 2026-11-05
layer: procedural
cues: rename, refactor, addendum, leftover-audit
---
Read the rename spec, then re-read it and any addendum before finishing: requirements can be amended mid-task. Edit in batches by concern (calls, named/as/star imports, attribute refs, getattr and patch targets, generated protos, docs). Then audit leftovers: every surviving old-name occurrence must be intentional, and every bare old-name use must have a binding (import or attribute).
