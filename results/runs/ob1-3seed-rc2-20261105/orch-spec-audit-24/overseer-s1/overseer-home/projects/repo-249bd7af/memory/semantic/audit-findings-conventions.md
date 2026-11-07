---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e255
added: 2026-11-05
cues: findings, audit-reports, clause-order, lfs-pointers, unverifiable
valid_from: 2026-11-05T23:46:53Z
---
Audit reports live in findings/, one JSON per service (svc-NN.json). List violations in spec clause order; compliant services have no violations. If a service's source files are Git LFS pointers, treat it as unverifiable: report no violations, never as compliant or violating.
