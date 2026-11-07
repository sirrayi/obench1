---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e442
added: 2026-11-05
cues: TICKETS/, tests, pytest, CHANGELOG
valid_from: 2026-11-05T14:28:12Z
---
CONTRIBUTING.md is the authoritative rulebook; read it first. Tickets are markdown files in TICKETS/, one per ticket, and can arrive mid-task. Tests live in tests/ and run with python3 -m pytest -q or python3 -m unittest discover -s tests -t . . CHANGELOG.md has an Unreleased section with one entry per ticket in ticket-number order. Each changed function carries its ticket marker on the def line. The checkout is shared with other people; the state at finish is what gets checked.
