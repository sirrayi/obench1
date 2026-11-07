---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e128
added: 2026-11-06
cues: translation, _(), Python 3.6, typing
valid_from: 2026-11-06T00:26:33Z
---
User-facing strings in the `web` package go through `_()` as translated templates; do not hardcode English text. The `edge` package must remain Python 3.6-compatible: use `typing` hints and avoid syntax newer than 3.6.
