---
provenance: review:session:p2 tainted:review
confidence: 0.6
source: overseer:session/p2#e125
added: 2026-11-05
layer: semantic
cues: tally, top, expenses, sorting, ties
---
`tally top N` prints the N largest expenses largest-first, one per line as `<date> <amount> <category>` with the amount at 2 decimals. Ties go to the earlier date. N <= 0 prints nothing; a non-integer N is a usage error (exit 2).
