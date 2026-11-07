---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e191
added: 2026-11-05
cues: money, Decimal, rounding, currency, CSV export
valid_from: 2026-11-05T05:15:42Z
---
invoicer money handling: multiply decimal strings exactly with Decimal, round each line half-up to cents via Decimal.quantize, then sum the rounded lines. CLI --currency defaults to EUR and supports USD and GBP, printing the prefix symbol. CSV export is invoicer/export.py to_csv.
