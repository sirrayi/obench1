---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e171
added: 2026-11-05
cues: record normalizer, spec rules, examples, normalization
valid_from: 2026-11-05T23:17:44Z
---
Read specs/RULES.md and each service's examples/ first. Share rule application in one engine module; each service file keeps only its literal ordered rule list and a thin normalize(record) -> dict. Apply rules in order to a copy, never mutating the input. Re-read specs before finishing: they change mid-task and the current spec wins. Run every worked example. Pitfalls: parse money with Decimal and half-up rounding; booleans accept spaced and dash variants; dates are DD/MM/YYYY; resolve cross-service dependencies before comparing.
