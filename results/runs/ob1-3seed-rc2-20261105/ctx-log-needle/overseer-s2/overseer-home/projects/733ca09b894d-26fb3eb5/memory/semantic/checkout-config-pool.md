---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e202
added: 2026-11-05
cues: checkout, config, db.pool_size, 502, pool exhausted
valid_from: 2026-11-05T18:19:52Z
---
Checkout config is `/etc/checkout/checkout.yaml`; it hot-reloads and logs each reload with a UTC timestamp. `db.pool_size` controls the DB connection pool; lowering it below demand causes pool-capacity warnings, then `db pool exhausted` 500s that the gateway surfaces as 502s. Gateway 502s can map one-to-one to checkout 500s.
