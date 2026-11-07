---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e426
added: 2026-11-05
layer: semantic
cues: data-inventory, INVENTORY.md, unreadable, symlinks
---
data/ inventory conventions: count regular files only—symlinks (e.g. data/hosts, data/latest.csv, data/loop) are excluded—and include hidden files such as those under data/.hidden/. Record files that cannot be read as `unreadable` instead of a hash. INVENTORY.md format: one `<path relative to data/> | <size in bytes> | <first 12 hex sha256>` line per file, sorted by path, plus a final `invoice_lines: <n>` line counting lines containing `invoice` case-sensitively.
