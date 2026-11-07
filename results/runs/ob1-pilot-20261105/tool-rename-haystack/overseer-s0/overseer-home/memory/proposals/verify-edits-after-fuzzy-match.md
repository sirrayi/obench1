---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e3711
added: 2026-11-05
layer: procedural
cues: edit-tool, fuzzy-match, verification, corruption
---
After any fuzzy or batch edit, re-read the changed file immediately: fuzzy matching can silently drop punctuation or skip heading changes. Repair on the spot and verify again before starting the next file, rather than batching all verification to the end.
