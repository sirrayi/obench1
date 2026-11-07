---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e193
added: 2026-11-05
layer: semantic
cues: read, redaction, hashes, run_code
---
The read tool redacts hash-like fields (e.g., git commit hashes) in file contents; run_code sees the real values. Compute on such data inside run_code and mask values before printing for review.
