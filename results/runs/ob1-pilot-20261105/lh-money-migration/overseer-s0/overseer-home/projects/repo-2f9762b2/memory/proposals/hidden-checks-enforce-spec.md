---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e2825
added: 2026-11-05
layer: semantic
cues: tests, hidden-checks, spec
---
The visible suite is `python3 -m unittest discover -s tests -t .`, but hidden checks far outnumber it and enforce the rules in `MIGRATION.md` — validate against the spec rather than relying on green visible tests.
