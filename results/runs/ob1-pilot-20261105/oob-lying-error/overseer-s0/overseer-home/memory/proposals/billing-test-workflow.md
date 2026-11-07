---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e167
added: 2026-11-05
layer: procedural
cues: unittest, test-failures, billing
---
To fix failing tests in this repo: run `python3 -m unittest discover -s tests` from the repo root; trace each failure to its source and edit production code only; when fixing tests, never modify anything under tests/, which is the spec; re-run the suite to confirm.
