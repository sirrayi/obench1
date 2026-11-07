---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e349
added: 2026-11-05
layer: semantic
cues: legacy.py, latin-1, encoding, non-utf8
---
src/legacy.py is latin-1 encoded, not UTF-8, so UTF-8-assuming read/edit calls fail on it. Read and rewrite it with explicit latin-1 decode/encode, then re-read to confirm the change landed and that no unrelated bytes shifted.
