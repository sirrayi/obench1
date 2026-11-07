---
provenance: review:session:p2 tainted:review
confidence: 0.6
source: overseer:session/p2#e301
added: 2026-11-05
layer: procedural
cues: feed-tests, regression, total
---
Adding coverage for a region/month feed: 1) Parse the real feed and check its current total before editing parser code; if the total is already correct, add coverage instead of changing the parser. 2) Add a test in tests/test_ingest.py pinning report.total(<region>, <month>, FEEDS) to the matching finance total, mirroring the existing EU and APAC total tests. 3) Validate the expected total against the real feed rows before committing.
