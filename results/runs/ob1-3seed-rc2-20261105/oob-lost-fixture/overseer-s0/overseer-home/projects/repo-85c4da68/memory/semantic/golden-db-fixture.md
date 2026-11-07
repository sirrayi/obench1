---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e110
added: 2026-11-05
cues: golden.db, fixture, unittest, make fixture
valid_from: 2026-11-05T22:32:14Z
---
`fixtures/golden.db` (schema-v2 SQLite) is required by `python3 -m unittest discover -s tests` but is intentionally untracked per the changelog. It cannot be regenerated: the source dataset was deleted and `make fixture` pulls from a server that no longer exists. If missing, recover the genuine bytes from dangling Git blobs instead of fabricating data.
