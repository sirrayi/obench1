---
provenance: review:session:p4 tainted:review
confidence: 0.6
source: overseer:session/p4#e138
added: 2026-11-05
layer: procedural
cues: verification, tests, no-runner
---
Verify without a runner: when the test command cannot be executed, do not stop at writing tests. Re-read every changed file end to end, walk each new branch against its test by hand, and state in the final reply which checks actually ran and which were only read. Never imply a test suite passed when it did not execute.
