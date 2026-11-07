---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e162
added: 2026-11-05
cues: spec implementation, test coverage, leap year, independent verification
valid_from: 2026-11-05T07:21:38Z
---
Implementing a module to a SPEC.md: read the spec and list every required behavior; implement it; then write tests in tests/ covering each clause, including boundaries such as leap February and year-crossing ISO weeks. Recompute expected values independently (reimplement the logic in a runnable runtime and run every case) because hand-computed expectations drift. Never assert behavior the spec leaves unspecified; document the chosen behavior instead.
