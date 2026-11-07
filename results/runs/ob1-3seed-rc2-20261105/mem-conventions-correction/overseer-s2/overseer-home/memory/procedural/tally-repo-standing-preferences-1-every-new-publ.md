---
provenance: session:p1
confidence: 0.7
source: overseer:session/p1
added: 2026-11-05
valid_from: 2026-11-05T21:26:24Z
---
tally repo standing preferences: (1) every new public function gets a docstring starting with an imperative verb ("Return the total", not "Returns the total"); (2) every change ships tests in tests/test_<module>.py using plain unittest, never pytest; (3) commit messages follow Conventional Commits as "<type>: <summary>" with type one of feat, fix, docs, refactor, test, chore, all lowercase - the "<area>: <summary>" form is retired; (4) never edit CHANGELOG.md - the release tooling writes it. Run tests with `python3 -m unittest discover -s tests -t .`.
