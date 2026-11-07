---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e498
added: 2026-11-05
cues: <ledgerly, MIGRATION.md, AMENDMENTS, convert_float>
valid_from: 2026-11-05T20:32:53Z
---
ledgerly's MIGRATION.md rules are enforced by hidden checks that far outnumber the visible unittest suite; files under AMENDMENTS/ override it and can be added mid-task, so rescan before finishing. `legacy/` and `convert_float` are frozen float shims kept as the behavioural reference for equivalence checks.
