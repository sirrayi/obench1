---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e1047
added: 2026-11-05
layer: semantic
cues: checkout, 502, db-pool, config
---
checkout: keep db.pool_size at 40 — lowering it (e.g., to 4) exhausts the DB connection pool and produces gateway 502s whose log entries cite db pool exhaustion. If 502s mention the DB pool, check db.pool_size before other config; other changes in the same reload can be unrelated.
