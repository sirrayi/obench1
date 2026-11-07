---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e3711
added: 2026-11-05
layer: procedural
cues: proto, genproto, codegen, byte-for-byte
---
When regenerating proto-derived Python, use tools/genproto.py's renderer rather than ad-hoc output, and first reproduce an existing checked-in generated file byte-for-byte to validate the renderer before writing new artifacts.
