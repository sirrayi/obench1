---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e196
added: 2026-11-05
cues: clients package, _rules, normalize signature
valid_from: 2026-11-05T22:59:31Z
---
`clients/` holds one module per spec service (`accounts`, `billing`, `contacts`, `customers`, `invoices`, `payments`, `returns`, `shipments`), each exposing `normalize(record: dict) -> dict`; shared rule primitives live in `clients/_rules.py`; dependent services reuse by calling the upstream service's normalize rather than reimplementing its rules.
