---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e193
added: 2026-11-05
layer: procedural
cues: release-notes, commits, mailmap, breaking-changes
---
Release notes (RELEASE_NOTES.md) from commits.jsonl: exclude reverts and the commits they name; treat `!` or BREAKING CHANGE as breaking; keep feat/fix/perf plus breaking commits; drop malformed headers and non-breaking internal scopes; fold perf into Features as `[perf]`; render deps as dependencies; merge duplicate change groups; truncate long summaries; sort by scope then time; build sections in order (Breaking changes, Features, Fixes, Performance, Contributors), omitting empty ones; normalize contributors (authors and co-authors) via .mailmap. Follow explicit rules if different.
