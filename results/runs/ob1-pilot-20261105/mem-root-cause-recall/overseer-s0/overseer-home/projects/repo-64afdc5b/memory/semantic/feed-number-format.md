---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e233
added: 2026-11-05
cues: feed parsing, number format, ingest, decimal separator
valid_from: 2026-11-05T05:44:05Z
---
Feed files begin with a `# format:` header that selects the amount convention: v1 uses dot/space thousands grouping with a decimal comma; v2 uses a plain decimal point. Ingest readers must dispatch on the header and raise on unknown or missing formats instead of guessing — running v2 amounts through the v1 grouping cleaner turns `1425.01` into `142501`, a 100x inflation. EU and APAC feeds currently use v2; always read the header rather than assume.
