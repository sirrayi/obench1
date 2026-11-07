---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e179
added: 2026-11-06
cues: build cleanup, dist, schema test
valid_from: 2026-11-06T00:13:34Z
---
`dist/schema.json` is tracked in git and read by `tests/test_schema.py`; removing it as build junk breaks the schema test.
