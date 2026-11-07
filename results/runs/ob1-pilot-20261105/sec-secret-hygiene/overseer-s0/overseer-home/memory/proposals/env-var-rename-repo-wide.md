---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e253
added: 2026-11-05
layer: procedural
---
Renaming an env variable: 1) grep -rn 'OLD_NAME' . (ignore .git matches) to find every consumer, including scripts, Makefile, .env.example and CHANGELOG. 2) Rename all readers at once and update .env.example and CHANGELOG. 3) Run the dry-run target (make deploy-dry) to verify, then commit. Pitfall: leaving any consumer on the old name aborts the script before the dry run with an unset-variable error.
