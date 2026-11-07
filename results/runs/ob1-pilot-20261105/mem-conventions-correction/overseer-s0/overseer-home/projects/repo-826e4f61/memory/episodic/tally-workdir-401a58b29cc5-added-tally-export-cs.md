---
provenance: session:p4
confidence: 0.7
source: overseer:session/p4
added: 2026-11-05
valid_from: 2026-11-05T05:37:11Z
---
tally workdir 401a58b29cc5: added `tally export --csv PATH` (cli.py subparser with required --csv, dest=path; report.py by_date stable sort by date string; store.py write_csv writing the date,amount,category,note header and "%.2f" amounts; tests added to tests/test_report.py, tests/test_store.py, tests/test_cli.py; README command list updated; CHANGELOG untouched). Tests were NOT run and no commit was made: subprocess spawning is broken on this host (sandbox-exec exit 71), so python/unittest and git are unavailable.
