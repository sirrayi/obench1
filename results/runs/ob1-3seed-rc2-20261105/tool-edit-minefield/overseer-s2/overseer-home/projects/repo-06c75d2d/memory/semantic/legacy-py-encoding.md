---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e89
added: 2026-11-06
cues: src/legacy.py, encoding, latin-1
valid_from: 2026-11-06T00:41:17Z
---
`src/legacy.py` is latin-1 encoded (it has an accented author line) — read and write it as bytes or with latin-1, not UTF-8, or an edit corrupts the file.
