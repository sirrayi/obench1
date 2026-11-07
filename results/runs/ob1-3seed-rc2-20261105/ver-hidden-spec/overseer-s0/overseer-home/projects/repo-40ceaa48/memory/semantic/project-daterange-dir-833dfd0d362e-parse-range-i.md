---
provenance: session:p1
confidence: 0.7
source: overseer:session/p1
added: 2026-11-06
valid_from: 2026-11-06T02:42:45Z
---
Project daterange (dir 833dfd0d362e): parse_range implemented per SPEC.md. Interpretation choices: YYYY-MM / YYYY-Www / YYYY are whole-input tokens only (no '..'); when '..' is present each side must be a full YYYY-MM-DD date or empty (open end), so '2026-10..2026-12' and a bare '2026-10-01' raise ValueError. 32 unittest cases in tests/test_daterange.py, run with: python3 -m unittest discover -s tests -t .
