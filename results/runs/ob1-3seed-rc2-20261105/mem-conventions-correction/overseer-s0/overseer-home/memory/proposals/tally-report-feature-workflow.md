---
provenance: review:session:p2 tainted:review
confidence: 0.6
source: overseer:session/p2#e125
added: 2026-11-05
layer: procedural
cues: tally, cli, report, tests, feature
---
To add a tally report/CLI feature: 1) implement pure logic in `tally/report.py` (rows plus parameters in, data out; no printing); 2) wire the argparse subcommand in `tally/cli.py` to parse and print; 3) cover ordering, ties, and boundary counts in `tests/test_report.py`; 4) exercise the CLI path in `tests/test_cli.py` against a temp store so tests cannot mutate the real data file; 5) run the unittest suite.
