---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e124
added: 2026-11-05
cues: proration, rounding, billing, half up, credits
valid_from: 2026-11-05T22:49:38Z
---
Billing proration rounds half up using exact integer arithmetic: (2*amount_cents*days_used + days_in_period) // (2*days_in_period). Never use int() truncation or floats; ties and credits round up identically.
