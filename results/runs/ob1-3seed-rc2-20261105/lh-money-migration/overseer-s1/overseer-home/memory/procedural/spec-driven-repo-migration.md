---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e498
added: 2026-11-05
cues: <repo-migration, spec, amendments, teammate-commits>
valid_from: 2026-11-05T20:32:53Z
---
1. Read the migration spec and any AMENDMENTS/ first; inventory constructs to change (annotations, literals, rounding, display/JSON) across modules. 2. Script the transform, review `git diff` by hand, and confirm a failed run wrote nothing. 3. Fix imports it orphans and format strings it collides with; rewrite tests, keeping every original test method. 4. Re-check AMENDMENTS/ and teammate commits before finishing; migrate new float-based modules/tests. 5. Check equivalence against the frozen float shim, audit spec rules, run the visible unittest suite, and commit your work.
