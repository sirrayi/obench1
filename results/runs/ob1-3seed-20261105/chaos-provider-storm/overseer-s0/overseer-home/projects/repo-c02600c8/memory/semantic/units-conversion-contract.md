---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e182
added: 2026-11-05
cues: units, convert, conversion, cli, kelvin, ValueError
valid_from: 2026-11-05T13:53:12Z
---
`units` package: README.md is the spec. `convert(value, src, dst)` uses exact factors for length (m, km, cm, mi, ft, in) and mass (kg, g, lb, oz); temperatures C/F/K route affinely through kelvin. Unit names are case-sensitive; raise ValueError for unknown units, cross-dimension conversion, and temperatures below absolute zero. CLI `python3 -m units <value> <src> <dst>` prints results with `%.6g` and writes errors to stderr with exit status 2.
