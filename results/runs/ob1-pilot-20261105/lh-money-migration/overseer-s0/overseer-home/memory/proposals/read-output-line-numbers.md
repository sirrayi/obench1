---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e2825
added: 2026-11-05
layer: procedural
cues: read, line-numbers, write, repair
---
Never write `read` output back to disk: it carries line-number prefixes that embed into files and double-prefix on repair. Strip prefixes with a fixed-point loop across all files until a pass changes nothing.
