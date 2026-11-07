---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e177
added: 2026-11-05
cues: worker.py, chunks, test_chunks
valid_from: 2026-11-05T19:28:21Z
---
relay/worker.py chunks() must include the final partial batch; dropping the trailing partial batch fails test_chunks.
