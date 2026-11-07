---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e128
added: 2026-11-06
cues: since, skipped, temp None, export note
valid_from: 2026-11-06T00:26:33Z
---
In `edge.uploader.upload` and `web.export.export`, the optional `since` argument (YYYY-MM-DD) filters first: readings from earlier days are dropped, then readings with `temp` None are skipped and counted as `skipped`. `web.export.export` adds `note` only when `skipped` > 0, using the translated template "<n> readings skipped (no temperature)". Keep existing return keys (`sent`/`payload`, `title`/`rows`).
