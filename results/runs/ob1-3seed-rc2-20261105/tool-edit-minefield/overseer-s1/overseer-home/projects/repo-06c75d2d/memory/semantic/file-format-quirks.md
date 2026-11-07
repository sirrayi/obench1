---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e136
added: 2026-11-06
cues: file quirks, encoding, latin-1, bom, minified json, app.ini sections
valid_from: 2026-11-06T00:39:21Z
---
Editing gotchas: src/legacy.py is Latin-1 encoded and defines recalc, a separate function from calc; notes/README.txt has a UTF-8 BOM and no trailing newline; data/catalog.min.json is a single minified line — edit in place, never reformat; config/app.ini defines timeout in multiple sections ([server], [client], [cache]), so key changes must be scoped to the right section.
