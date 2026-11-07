---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e89
added: 2026-11-06
cues: config/app.ini, server timeout, crlf
valid_from: 2026-11-06T00:41:17Z
---
`config/app.ini` uses CRLF line endings — preserve them on any edit. Its `[server]` section carries a `timeout` distinct from the separate client and cache timeouts; change only the one named.
