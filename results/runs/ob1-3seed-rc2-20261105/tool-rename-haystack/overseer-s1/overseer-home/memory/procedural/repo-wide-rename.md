---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e405
added: 2026-11-06
cues: git grep, rename, mock.patch, baseline
valid_from: 2026-11-06T01:19:56Z
---
1) Read the spec; re-read it before finishing (review may append an addendum mid-task). 2) Clean tree + green test baseline. 3) Sweep: `git grep -n NAME -- ':!logs/'`; a bare grep chokes on huge logs. 4) Classify each shape: multi-line imports, mock.patch targets, getattr/handler strings, star imports. 5) Script the rewrite outside the checkout; regenerate generated code from source. 6) Verify: suite green, added/removed diff lines symmetric, residuals are intended keepers. Pitfalls: renaming NAME mangles NAME_count — use word boundaries, grep mangled variants; re-baseline when HEAD moves.
