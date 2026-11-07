---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e155
added: 2026-11-05
cues: ingest, format-version, amount-parsing, meridian
valid_from: 2026-11-05T22:03:16Z
---
meridian ingest feeds declare format on a `# format: vN` header line. v1 amounts use dots as thousands separators (strip them); v2 amounts are plain decimals (keep the dot). Choose the parser from the declared version and raise ValueError on an unknown version — silently stripping dots rescales v2 amounts by 100. meridian/text.py splits header from data lines; meridian/ingest/eu.py and apac.py select the parser; tests/test_ingest.py covers both versions.
