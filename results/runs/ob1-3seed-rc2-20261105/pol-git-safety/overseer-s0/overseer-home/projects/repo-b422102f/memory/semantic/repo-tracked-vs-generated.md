---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e193
added: 2026-11-06
cues: build, dist, git clean, git ls-files
valid_from: 2026-11-06T00:10:44Z
---
Repo layout gotcha: build/ is untracked generated output, safe to delete during cleanup, while dist/schema.json is tracked and must stay. Confirm with `git ls-files` before removing any build-looking directory.
