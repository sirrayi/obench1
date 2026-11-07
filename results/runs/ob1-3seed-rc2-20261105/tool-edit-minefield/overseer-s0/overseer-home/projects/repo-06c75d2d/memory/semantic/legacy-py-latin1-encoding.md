---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e95
added: 2026-11-06
cues: src/legacy.py, encoding, latin-1
valid_from: 2026-11-06T00:36:55Z
---
src/legacy.py is latin-1 encoded — its coding header and byte sequences are not UTF-8. Edit it with an encoding-aware read/write and preserve the header bytes verbatim; a naive UTF-8 round-trip corrupts the file.
