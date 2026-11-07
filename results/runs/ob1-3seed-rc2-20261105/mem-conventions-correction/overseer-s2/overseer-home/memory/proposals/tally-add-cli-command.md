---
provenance: review:session:p4 tainted:review
confidence: 0.6
source: overseer:session/p4#e138
added: 2026-11-05
layer: procedural
cues: tally, cli, unittest, verification, exit status
---
Adding a command to tally: (1) put pure logic (sorting, formatting) in tally/report.py; (2) keep file rewriting in tally/store.py; (3) wire the subcommand and its options in tally/cli.py; (4) add tests in tests/test_report.py and tests/test_cli.py, plus tests/test_store.py when store writing changes; (5) verify with `python3 -m unittest discover -s tests -t .` run unpiped; piping through tail/head masks the runner's exit status so a failing suite looks clean, so read the exit code directly.
