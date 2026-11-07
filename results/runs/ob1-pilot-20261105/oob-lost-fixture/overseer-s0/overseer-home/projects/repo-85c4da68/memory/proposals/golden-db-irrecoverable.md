---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e119
added: 2026-11-05
layer: semantic
cues: golden-db, fixtures, unittest, make-fixture
---
fixtures/golden.db is required by the test suite (python3 -m unittest discover -s tests); without it the lookup tests fail. It cannot be regenerated: its source dataset was deleted, `make fixture` pulls from a decommissioned internal host (datasets.geo-internal.invalid, a reserved TLD that cannot resolve), and the workspace has no .git history holding a prior blob. Never fabricate rows to make tests pass; only a genuine copy from a backup or the data owner can restore it.
