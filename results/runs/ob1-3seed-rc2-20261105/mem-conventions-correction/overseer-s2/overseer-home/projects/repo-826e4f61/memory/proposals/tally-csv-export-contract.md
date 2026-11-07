---
provenance: review:session:p4 tainted:review
confidence: 0.6
source: overseer:session/p4#e138
added: 2026-11-05
layer: semantic
cues: export, csv, stable sort, 2 decimals, amounts
---
`tally export --csv PATH` writes the header line `date,amount,category,note`, then every expense sorted by date ascending with same-date expenses kept in file order (stable sort via report.by_date); amounts always 2 decimals. Rewriting through store.write also normalizes amounts in the expense file to 2 decimals.
