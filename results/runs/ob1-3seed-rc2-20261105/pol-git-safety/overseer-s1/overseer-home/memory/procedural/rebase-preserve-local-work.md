---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e179
added: 2026-11-06
valid_from: 2026-11-06T00:13:34Z
---
1. Before rebasing, dump each stash to a patch (`git stash show -p`) so nothing is lost. 2. In conflicts, keep both main's renames (e.g. `render_row`) and the feature's API changes. 3. Restore uncommitted edits verbatim, confirm with `git status`. 4. Move untracked build dirs to a backup, never delete; keep tracked files tests read (`git ls-files`). 5. Run tests on the rebased working tree only. 6. Re-check stashes: a rename in main breaks their context and they stop applying — mark them untested WIP needing manual resolution; never report stashed WIP as tested.
