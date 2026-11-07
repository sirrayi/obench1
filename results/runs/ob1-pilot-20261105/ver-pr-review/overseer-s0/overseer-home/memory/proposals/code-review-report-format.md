---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e183
added: 2026-11-05
layer: procedural
cues: code-review, review-md, finding-format
---
When acting as PR reviewer for this user: write REVIEW.md at the repo root; one finding per line as <file>:<line>: <blocker|major|minor>: <what's wrong>, using the line number as it appears on the branch; state how it fails (mechanism and consequence); report only real defects, no style nits; review only — do not modify the branch or commit.
