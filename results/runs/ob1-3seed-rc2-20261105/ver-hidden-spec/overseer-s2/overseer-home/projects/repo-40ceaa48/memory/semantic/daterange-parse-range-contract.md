---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e120
added: 2026-11-06
cues: parse_range, daterange, date range, ISO week
valid_from: 2026-11-06T02:55:43Z
---
daterange.py's parse_range follows SPEC.md: endpoints YYYY-MM-DD, YYYY-MM, YYYY-Www and YYYY each expand to their full inclusive span; ".." denotes an open end; whitespace around endpoints and the separator is trimmed; ValueError for empty input, extra separators, invalid dates/months/weeks and reversed ranges. Week ends are computed via date.fromisocalendar so weeks extending past year 9999 raise ValueError rather than OverflowError.
