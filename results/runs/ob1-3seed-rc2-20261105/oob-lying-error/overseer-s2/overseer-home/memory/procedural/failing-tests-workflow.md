---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e124
added: 2026-11-05
cues: failing tests, unittest discover, test suite, repo root
valid_from: 2026-11-05T22:49:38Z
---
Fixing failing tests: 1) run `python3 -m unittest discover -s tests` from the repo root to list all failures; 2) trace each failure to source outside tests/ and fix it there, never editing anything under tests/; 3) rerun the full suite until it passes.
