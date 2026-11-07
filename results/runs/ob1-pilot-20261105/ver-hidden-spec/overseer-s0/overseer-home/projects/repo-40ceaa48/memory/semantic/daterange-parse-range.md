---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e162
added: 2026-11-05
cues: parse_range, daterange, spec semantics
valid_from: 2026-11-05T07:21:38Z
---
`daterange.py` `parse_range` semantics: split the input on the first `..` only and join the left span's first day to the right span's last day; either side may be omitted (open start/end). A term expands to an inclusive day span: full ISO date (bare date = one-day range), `YYYY-MM` (leap-aware calendar month), `YYYY-Www` via `date.fromisocalendar` (handles year-crossing weeks and W53), or `YYYY` (whole year). `..` alone, unknown terms and reversed ranges raise `ValueError`.
