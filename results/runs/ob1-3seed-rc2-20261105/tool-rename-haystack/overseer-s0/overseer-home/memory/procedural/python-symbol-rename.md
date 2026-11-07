---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e377
added: 2026-11-06
cues: rename, symbol-rename, refactor
valid_from: 2026-11-06T00:56:37Z
---
Symbol rename: read the spec; re-read it before final verification (review may amend mid-task); re-check HEAD before editing and at the end (teammates land commits; final checkout gets checked). Keep transformation scripts outside the repo. Grep every reference form: calls, imports (plain/as/star), attribute lookups, getattr strings, mock.patch targets, default args, functools.partial, handler strings. Keep the old name as a deprecation wrapper with the documented warning, old kwargs still accepted/forwarded, out of __all__, new name in. Verify by recomputing the intended diff from HEAD.
