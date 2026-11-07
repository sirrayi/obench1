---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e2825
added: 2026-11-05
layer: semantic
cues: money, decimal, rounding, rates, json
---
Ledgerly money values are `Money`/`Decimal`, never float: sums via `Money.sum`, JSON via `to_json()` objects, text formatting rounds without floats. Each package has its own rounding mode; payouts use ROUND_HALF_EVEN. `RATES` is built from the CSV text by the generator script; `MoneyF`/`Rate` are gone from types.py and `legacy/` is out of scope.
