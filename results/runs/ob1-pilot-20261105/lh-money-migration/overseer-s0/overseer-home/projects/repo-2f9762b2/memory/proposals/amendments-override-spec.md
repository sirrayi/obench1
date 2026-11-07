---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e2825
added: 2026-11-05
layer: semantic
cues: amendments, migration, concurrent, drift
---
`AMENDMENTS/` decisions override `MIGRATION.md`; read both before starting and re-check before finishing. Teammates commit to the branch concurrently, so re-scan the whole tree (HEAD, new modules, new amendments) before final verification — the repo state at finish is what gets checked.
