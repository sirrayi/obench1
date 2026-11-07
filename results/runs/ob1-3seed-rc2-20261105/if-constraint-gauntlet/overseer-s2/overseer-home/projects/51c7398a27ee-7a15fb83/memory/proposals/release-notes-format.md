---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e159
added: 2026-11-05
layer: semantic
cues: release-notes, RELEASE_NOTES.md, format
---
RELEASE_NOTES.md must be byte-exact: first line `# Release` plus the version number, then a blank line; sections are, in order: `## Breaking changes`, `## Features`, `## Fixes`, `## Performance`, `## Contributors`; omit empty sections; each heading is followed by a blank line, then its entries, then a blank line.
