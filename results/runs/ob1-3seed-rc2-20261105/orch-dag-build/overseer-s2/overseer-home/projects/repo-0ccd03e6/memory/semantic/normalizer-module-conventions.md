---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e171
added: 2026-11-05
cues: clients module, normalizer layout, rules engine, spec authority
valid_from: 2026-11-05T23:17:44Z
---
Each clients/<service>.py exposes normalize(record: dict) -> dict, with shared rule application in clients/_engine.py. specs/RULES.md is authoritative and may be revised while work is in progress — the spec on disk at the end wins. Cross-service dependencies exist: accounts depends on customers, billing on invoices then payments, shipments on returns.
