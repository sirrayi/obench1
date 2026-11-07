---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e229
added: 2026-11-05
layer: procedural
cues: normalizers, clients, specs, examples
---
Steps: read specs/RULES.md and the service spec; write clients/<service>.py exposing normalize(record: dict) -> dict; implement the rules in the exact order the spec lists them; keep each file self-contained with helpers inlined (cents via Decimal half-up, bool, iso-date, split); hand-check every worked case in examples/; re-read specs for amendments before declaring done.
