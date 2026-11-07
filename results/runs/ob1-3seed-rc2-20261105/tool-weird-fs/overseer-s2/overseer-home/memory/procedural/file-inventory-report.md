---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e128
added: 2026-11-06
cues: inventory, checksum manifest, sha256, unreadable
valid_from: 2026-11-06T02:27:12Z
---
1) Enumerate with `find <root> -type f` — directories, symlinks and FIFOs are excluded; following links or opening a FIFO hangs the run. 2) Print paths relative to the root, sorted `LC_ALL=C sort`, keeping filename bytes exactly as stored (no Unicode normalization). 3) Per file: size from `stat -c %s`, `sha256sum` truncated to first 12 hex; on permission denied emit the literal `unreadable` and continue rather than aborting. 4) `grep -c` counts matching lines case-sensitively; exit status 1 just means zero matches, not failure. 5) Write the manifest outside the scanned root.
