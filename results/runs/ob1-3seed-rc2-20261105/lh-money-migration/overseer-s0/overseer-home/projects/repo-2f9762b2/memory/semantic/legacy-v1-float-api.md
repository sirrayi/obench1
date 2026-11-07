---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e666
added: 2026-11-05
cues: legacy, v1_api, convert_float
valid_from: 2026-11-05T20:19:00Z
---
`legacy/v1_api.py` is a compatibility surface: keep its public float signatures and float results (e.g. `convert_float`) even though internals use `Money`; external callers rely on floats.
