---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e426
added: 2026-11-05
layer: procedural
cues: file-inventory, sha256, line-count, filenames
---
When inventorying a directory with shell tools: enumerate regular files with `find <root> -type f` (no `-L`); quote each name and prefix it with `./` so leading-dash, space and bracket names aren't parsed as options or globs; compute SHA-256 with `shasum -a 256` and keep the first 12 hex; report apparent byte size (`wc -c` or `stat`), not disk blocks, for sparse files; count lines with `awk 'END{print NR}'` so a file without a trailing newline still counts its last line; count matching lines case-sensitively.
