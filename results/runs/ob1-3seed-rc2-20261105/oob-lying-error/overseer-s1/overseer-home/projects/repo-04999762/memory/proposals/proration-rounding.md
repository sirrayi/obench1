---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e106
added: 2026-11-05
layer: semantic
cues: billing, rounding, proration
---
Billing and proration math rounds to the nearest unit instead of truncating; partial periods and totals are computed with rounding so amounts do not drift.
