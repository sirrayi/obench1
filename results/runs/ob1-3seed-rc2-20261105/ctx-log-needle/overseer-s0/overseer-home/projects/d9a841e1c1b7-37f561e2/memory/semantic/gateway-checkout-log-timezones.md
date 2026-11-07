---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e182
added: 2026-11-05
cues: logs, gateway, checkout, timezone, CEST, UTC, 502
valid_from: 2026-11-05T17:54:10Z
---
`logs/` contains rotated gateway and checkout logs. Gateway timestamps are CEST (+0200); checkout logs are UTC. Normalize to one timezone before correlating events or reporting failure times.
