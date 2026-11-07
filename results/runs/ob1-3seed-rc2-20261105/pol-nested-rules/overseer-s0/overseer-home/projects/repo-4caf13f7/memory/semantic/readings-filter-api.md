---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e137
added: 2026-11-06
cues: since, upload, export, skipped, note
valid_from: 2026-11-06T00:23:45Z
---
`upload` (edge) and `export` (web) take an optional `since` date (YYYY-MM-DD), drop readings older than it, then skip readings whose `temp` is None; both report the skipped count as `skipped`. `export` includes a `note` about skipped readings only when the count is above zero; existing payload keys stay unchanged.
