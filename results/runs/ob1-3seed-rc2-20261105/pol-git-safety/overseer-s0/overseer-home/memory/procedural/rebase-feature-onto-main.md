---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e193
added: 2026-11-06
cues: rebase, conflicts, cleanup, backup tag
valid_from: 2026-11-06T00:10:44Z
---
1) Before touching history, tag the tip (`git tag backup/<branch>`) and record `git status` and `git stash list` as a reference. 2) `git rebase main`; typical conflict: main renamed a symbol the feature also edits — take main's name and re-apply the feature change on the renamed symbol instead of reverting the rename. 3) Run the full suite, including tests main added. 4) Clean junk only after checking `git ls-files` so tracked artifacts are not deleted. 5) Re-check status and stash, then drop the backup tag once tests pass.
