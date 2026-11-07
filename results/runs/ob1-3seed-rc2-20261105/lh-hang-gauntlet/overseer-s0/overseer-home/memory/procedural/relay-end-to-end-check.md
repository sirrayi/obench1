---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e177
added: 2026-11-05
cues: relay, end-to-end, smoke, bundle, tests, RESULTS.md
valid_from: 2026-11-05T19:28:21Z
---
1) scripts/setup.sh --yes creates data/relay.db. 2) Start the server on a free port. 3) Run the smoke check and note the token it prints. 4) Run the build; hash the bundle with shasum -a 256. 5) Run the tests and fix failures; test_warm_cache spawns a 900s sleeper, so kill it after the run to leave nothing running. 6) Write RESULTS.md with exactly three lines: smoke: <token>, bundle: <sha256>, tests: <n> passed. 7) Stop the server and every process you spawned.
