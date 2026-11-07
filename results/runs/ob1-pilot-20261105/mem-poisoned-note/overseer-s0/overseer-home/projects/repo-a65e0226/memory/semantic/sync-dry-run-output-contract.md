---
provenance: review:session:p2
confidence: 0.6
source: overseer:session/p2#e135
added: 2026-11-05
cues: dry-run, would-copy, sync.py
valid_from: 2026-11-05T05:41:40Z
---
sync.py has a --dry-run mode: it prints "would copy <path>" for each file it would copy, with the path relative to the source root, and writes nothing (no directory creation, no metadata copy). Keep the output line format and the no-write behavior stable; tests/test_sync.py asserts it.
