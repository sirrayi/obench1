---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e145
added: 2026-11-05
layer: semantic
cues: money, rounding, decimal, totals
---
invoicer money: use Decimal with ROUND_HALF_UP to cents per line, then sum the rounded line amounts; do not round the summed raw values.
