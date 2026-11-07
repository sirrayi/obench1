---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e666
added: 2026-11-05
cues: AMENDMENTS, MIGRATION.md, spec
valid_from: 2026-11-05T20:19:00Z
---
Specs can be amended: files under `AMENDMENTS/` override `MIGRATION.md`, so read both before changing spec-driven code. Acceptance checks follow the written rules (spec plus amendments) rather than the visible test suite; passing visible tests is not sufficient.
