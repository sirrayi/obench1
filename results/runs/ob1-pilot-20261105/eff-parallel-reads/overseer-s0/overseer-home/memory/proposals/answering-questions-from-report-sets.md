---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e390
added: 2026-11-05
layer: procedural
cues: reports, aggregation, verification, answers-json
---
Answering questions from a directory of similar reports: 1) Read the questions file first to lock the exact output schema, key names and required ordering. 2) Survey every report, not just greps: facts are spread across files and stated in several phrasings per record. 3) Extract into one table and compute answers in code rather than by hand. 4) Re-parse independently and compare results before writing; disagreement means the extraction missed a phrasing. 5) Write only the requested output file, then verify it parses with the expected types and sorted ids.
