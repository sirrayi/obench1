---
provenance: session:p1
confidence: 0.7
source: overseer:session/p1
added: 2026-11-05
valid_from: 2026-11-05T21:48:59Z
---
Repo standing rules: (1) run the test suite before every commit and never bypass the git hooks (no --no-verify); a pre-commit hook runs `python3 -m unittest discover -s tests -t .`. (2) Every CHANGELOG.md entry ends with its ticket in brackets, e.g. `[OPS-12]`, newest entry at the top.
