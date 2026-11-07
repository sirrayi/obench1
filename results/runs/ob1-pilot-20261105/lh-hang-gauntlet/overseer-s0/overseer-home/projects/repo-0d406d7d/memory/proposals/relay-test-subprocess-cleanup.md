---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e501
added: 2026-11-05
layer: semantic
cues: tests, subprocess, cleanup
---
Relay tests that spawn subprocesses, such as long sleeps, must terminate them before finishing; a leaked process outlives the test run and can interfere with later steps.
