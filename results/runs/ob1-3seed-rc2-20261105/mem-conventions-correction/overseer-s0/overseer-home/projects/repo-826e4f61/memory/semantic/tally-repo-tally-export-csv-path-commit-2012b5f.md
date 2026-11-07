---
provenance: session:p4
confidence: 0.7
source: overseer:session/p4
added: 2026-11-05
valid_from: 2026-11-05T21:05:50Z
---
tally repo: `tally export --csv PATH` (commit 2012b5f) writes expenses to PATH sorted by date, same-date rows keeping their file order, header from store.FIELDS ("date,amount,category,note"), amounts as "%.2f" of the Decimal. report.sorted_by_date(rows) does the stable sort; --csv is required, so a bare `export` exits 2. Tests live in tests/test_report.py (sorting, ties, empty) and tests/test_cli.py (file contents, missing path).
