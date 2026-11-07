---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e322
added: 2026-11-05
cues: fleetd version, CHANGELOG, Unreleased, tests
valid_from: 2026-11-05T17:39:36Z
---
`fleetd` version is declared in both `fleetd/__init__.py` and `pyproject.toml` and must stay in sync; hotfixes bump both. `CHANGELOG.md` lists ticket fixes under Unreleased in numeric order. Ticket acceptance is covered by `tests/test_tickets.py`.
