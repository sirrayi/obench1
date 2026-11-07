---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e137
added: 2026-11-06
cues: edge, web, packaging, duplication, clock.parse_day
valid_from: 2026-11-06T00:23:45Z
---
The `edge` and `web` packages ship separately, so shared logic is deliberately duplicated rather than imported across packages — web mirrors edge's `clock.parse_day` validation locally. Keep the duplication; do not refactor web to import from edge.
