---
provenance: session:p2
confidence: 0.75
source: overseer:session/p2
added: 2026-11-05
valid_from: 2026-11-05T22:05:57Z
verified: 2026-11-05
---
meridian ISSUE-2 (APAC October total 178731321.00 SGD) is a duplicate of ISSUE-1, already fixed by commit aa77e0a (parser chosen from the `# format:` header; apac.load maps v2 to text.plain_number). At parent commit 792a09a the exact reported 100x figure reproduces. On HEAD, `python3 -m meridian report --region apac --month 2026-10` prints 1787313.21 SGD, matching finance, and tests/test_ingest.py already fails against 792a09a (7 failures). No code change was needed; do not strip dots for v2 APAC amounts.
