---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e501
added: 2026-11-05
layer: semantic
cues: worker, chunks, tail
---
relay/worker.py chunks() must emit the final partial chunk; stopping one chunk early silently drops the tail, so assert the last chunk is included.
