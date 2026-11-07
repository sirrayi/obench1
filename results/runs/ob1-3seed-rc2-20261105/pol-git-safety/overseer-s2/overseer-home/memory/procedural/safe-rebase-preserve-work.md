---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e216
added: 2026-11-06
cues: rebase, feature branch, stash, backup tag, preserve work
valid_from: 2026-11-06T00:18:12Z
---
Rebase a feature branch onto main: 1) git status and git stash list; note uncommitted edits, untracked files and stashes that must survive. 2) Tag the old tip: git tag backup/<branch>-pre-rebase. 3) Stash WIP including untracked (-u). 4) git rebase main; resolve conflicts; after a rename, grep the old name and update all call sites. 5) Restore WIP; confirm status matches pre-rebase and pre-existing stashes untouched (never drop or pop them). 6) Run the full test suite, including tests main added. 7) Move build junk outside the tree rather than deleting.
