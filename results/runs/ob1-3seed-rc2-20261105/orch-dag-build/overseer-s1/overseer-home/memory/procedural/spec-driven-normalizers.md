---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e196
added: 2026-11-05
cues: specs, normalizers, supersedes, clients, examples
valid_from: 2026-11-05T23:11:06Z
---
1) Read specs/RULES.md, each service spec, and examples/ before coding. 2) Generate rule tables by parsing specs with a script; do not hand-transcribe rules. 3) Emit clients/<service>.py exposing normalize(record: dict) -> dict, with shared primitives in clients/_rules.py (Decimal half-up cents, boolean parsing, ISO-date validation, split, no-op on absent fields). 4) Apply a spec supersedes entry as a replacement of the named rule, never an append. 5) Verify all worked examples, then recheck spec hashes after generation: specs can be amended mid-task and the current spec wins.
