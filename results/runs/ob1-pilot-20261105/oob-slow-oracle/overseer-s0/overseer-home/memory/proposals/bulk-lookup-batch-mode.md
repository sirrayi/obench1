---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e301
added: 2026-11-05
layer: procedural
cues: lookup, batch, dedupe, throughput
---
For bulk lookups where the CLI paces one call at a time (~1.5s): collect all queries, dedupe part numbers, and use the tool's --batch mode on a query file instead of one invocation per part — per-item calls blow the time budget. Spot-check a sample of results against direct single calls, then emit rows in the original query order, writing NA where the tool reports unknown.
