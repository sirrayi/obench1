---
provenance: review:session:p3
confidence: 0.6
source: overseer:session/p3#e76
added: 2026-11-05
cues: --month, --category, tally sum
valid_from: 2026-11-05T21:04:11Z
---
`tally sum --month YYYY-MM` filters rows by comparing the stored date's `YYYY-MM` prefix; it composes with `--category`, and an unknown month totals 0. `report.total` performs this filtering.
