---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e193
added: 2026-11-05
layer: procedural
cues: byte-exact, verification, run_code, dry-run
---
For a file compared byte-for-byte: (1) read the spec and sources; (2) do all parsing and computation in run_code so intermediate values stay in code; (3) dry-run the full pipeline and review the result with hash-like values masked; (4) write only after in-code assertions for entry counts, uniqueness, and ordering; (5) re-read the written file and run an independent verification pass against the source.
