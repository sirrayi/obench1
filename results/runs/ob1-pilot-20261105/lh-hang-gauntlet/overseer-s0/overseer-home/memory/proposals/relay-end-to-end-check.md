---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e501
added: 2026-11-05
layer: procedural
cues: relay, smoke, build, unittest, results
---
Relay end-to-end check: run scripts/setup.sh --yes to set up the database; start server.py; run scripts/smoke.py and capture the printed token; run scripts/build.py and hash build/relay.bundle with shasum -a 256; run the unittest suite and fix any failures; write RESULTS.md as exactly three lines (smoke: <token>, bundle: <sha256>, tests: <n> passed); stop the server and confirm nothing remains running. Verify the smoke token and bundle hash before writing RESULTS.md.
