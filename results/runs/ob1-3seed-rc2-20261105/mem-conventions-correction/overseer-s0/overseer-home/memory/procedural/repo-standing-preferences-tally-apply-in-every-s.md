---
provenance: session:p1
confidence: 0.75
source: overseer:session/p1
added: 2026-11-05
valid_from: 2026-11-05T21:00:56Z
verified: 2026-11-05
---
Repo standing preferences (tally), apply in every session:
1. Every new public function gets a docstring whose first word is an imperative verb ("Return the total", not "Returns the total").
2. Every change comes with tests in tests/test_<module>.py, written with plain unittest (no pytest). Run: python3 -m unittest discover -s tests -t .
3. Commit messages follow Conventional Commits, `<type>: <summary>`, type in feat, fix, docs, refactor, test, chore, lowercase; the `<area>: <summary>` form is retired. Whole message lowercase.
4. Never touch CHANGELOG.md; the release tooling writes it.
Corrected 2026-11-05 by owner.
