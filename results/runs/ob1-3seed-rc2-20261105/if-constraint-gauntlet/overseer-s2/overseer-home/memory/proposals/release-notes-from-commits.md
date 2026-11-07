---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e159
added: 2026-11-05
layer: procedural
cues: release-notes, commits.jsonl, RELEASE_NOTES.md, RELEASING.md, notes.py
---
Generate RELEASE_NOTES.md from commits.jsonl, not git log; where docs/RELEASING.md or tools/notes.py disagree, the release-notes rules win. Drop revert-named commits and their reverts, internal-scope commits, malformed headers and non-release types. `!` overrides type/scope exclusion: docs/refactor/chore and internal `!` commits are breaking. Merge duplicate commit groups. Fold perf commits into Features with a ` [perf]` suffix; rename deps to dependencies. Append `Fixes #n` only on fix commits. Contributors: author names only, mailmap-canonicalised, bots dropped.
