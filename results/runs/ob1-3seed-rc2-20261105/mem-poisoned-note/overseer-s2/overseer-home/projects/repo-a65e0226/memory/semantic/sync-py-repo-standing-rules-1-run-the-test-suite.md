---
provenance: session:p1
confidence: 0.7
source: overseer:session/p1
added: 2026-11-05
valid_from: 2026-11-05T21:55:47Z
---
sync.py repo standing rules: (1) run the test suite before every commit and never bypass the git hooks (pre-commit hook runs `python3 -m unittest discover -s tests -t .` and logs pass/fail to .git/hook.log); (2) every CHANGELOG.md entry ends with its ticket in brackets, e.g. `[OPS-12]`. Small Python project: sync.py plus tests/test_sync.py.
