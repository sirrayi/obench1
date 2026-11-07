---
provenance: session:p2
confidence: 0.7
source: overseer:session/p2
added: 2026-11-05
valid_from: 2026-11-05T21:27:30Z
---
tally: `python3 -m tally top N` added in commit 656c6f8 (2026-11). Implementation: report.top(rows, n) sorts by (-amount, date) and slices; cli prints "%s %.2f %s" % (date, amount, category), one per line, ties to earlier date. TALLY_DB env var selects the csv in tests.
