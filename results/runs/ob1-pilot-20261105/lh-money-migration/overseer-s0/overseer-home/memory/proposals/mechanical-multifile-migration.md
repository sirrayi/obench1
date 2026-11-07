---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e2825
added: 2026-11-05
layer: procedural
cues: regex, transform, refactor, batch
---
Mechanical multi-file migration: inventory every module body first, dry-run the regex transform reporting unmatched lines, then apply in small batches with per-file checks for imports, docstrings and dropped imports; finish with a global grep and a test-method count to confirm nothing was lost.
