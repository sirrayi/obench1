---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e198
added: 2026-11-05
layer: semantic
cues: units, conversion, temperature, cli, error-handling
---
units package contract: `units.convert(value, src, dst)` raises ValueError for unknown units, case mismatches, and cross-dimension conversions. Temperatures (C/F/K) convert affinely through kelvin with an absolute-zero check plus a 1e-9 K slack so exactly -459.67 F is not rejected by float rounding. The CLI `python3 -m units <value> <src> <dst>` formats results with %.6g, writes errors to stderr, and exits 2.
