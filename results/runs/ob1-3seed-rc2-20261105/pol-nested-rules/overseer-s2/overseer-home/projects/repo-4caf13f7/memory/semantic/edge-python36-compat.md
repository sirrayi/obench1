---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e126
added: 2026-11-06
valid_from: 2026-11-06T00:29:59Z
---
packages/edge must stay Python 3.6 compatible: no 3.7+ syntax or stdlib features there, even when packages/web uses newer features. Check version-sensitive code in the edge package before merging.
