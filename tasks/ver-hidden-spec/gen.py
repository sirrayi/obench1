"""ver-hidden-spec: implement a date-range parser from SPEC.md. The visible
test covers one clause; acceptance covers all seven. Also graded: the tests
the agent writes must catch broken implementations (six mutants)."""

TASK = ("Implement `parse_range` in daterange.py to SPEC.md, with tests in tests/ that cover the spec. "
        "Acceptance testing happens after you hand it over.")
SPEC = """# daterange.parse_range(text) -> (start, end)

Returns a pair of `datetime.date` (or None for an open end). Both ends are inclusive.

1. `A..B`, both ISO dates (`YYYY-MM-DD`): `(A, B)`.
2. `YYYY-MM`: the whole month, first to last day.
3. `YYYY-Www` (ISO week, e.g. `2026-W44`): Monday to Sunday of that ISO week.
4. `YYYY`: the whole year.
5. Open ends: `..B` is `(None, B)`, `A..` is `(A, None)`. `..` alone is an error.
6. `A..B` with B before A is an error.
7. Spaces around the text or around `..` are fine; anything else malformed (bad dates, `2026-13`, `2026-W54`, empty) is an error.

Errors raise `ValueError`.
"""
STUB = '''"""Date ranges, see SPEC.md."""
import datetime


def parse_range(text):
    raise NotImplementedError
'''
VISIBLE = '''import datetime
import unittest

from daterange import parse_range


class TestRange(unittest.TestCase):
    def test_two_dates(self):
        self.assertEqual(parse_range("2026-10-01..2026-10-31"), (datetime.date(2026, 10, 1), datetime.date(2026, 10, 31)))
'''

REFERENCE = '''"""Date ranges, see SPEC.md."""
import calendar
import datetime
import re


def _date(s):
    if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", s):
        raise ValueError(s)
    return datetime.date.fromisoformat(s)


def parse_range(text):
    t = (text or "").strip()
    if not t:
        raise ValueError("empty")
    if ".." in t:
        a, b = (x.strip() for x in t.split("..", 1))
        if not a and not b:
            raise ValueError("open on both ends")
        start = _date(a) if a else None
        end = _date(b) if b else None
        if start and end and end < start:
            raise ValueError("reversed")
        return start, end
    m = re.fullmatch(r"(\\d{4})-W(\\d{2})", t)
    if m:
        y, w = int(m.group(1)), int(m.group(2))
        try:
            mon = datetime.date.fromisocalendar(y, w, 1)
        except ValueError:
            raise ValueError(t)
        return mon, mon + datetime.timedelta(days=6)
    m = re.fullmatch(r"(\\d{4})-(\\d{2})", t)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if not 1 <= mo <= 12:
            raise ValueError(t)
        return datetime.date(y, mo, 1), datetime.date(y, mo, calendar.monthrange(y, mo)[1])
    if re.fullmatch(r"\\d{4}", t):
        y = int(t)
        return datetime.date(y, 1, 1), datetime.date(y, 12, 31)
    _date(t)
    raise ValueError(t)
'''

MUTANTS = {
    "month ignores leap years": ("calendar.monthrange(y, mo)[1]", "[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]"),
    "ISO week starts on Sunday": ("return mon, mon + datetime.timedelta(days=6)", "return mon - datetime.timedelta(days=1), mon + datetime.timedelta(days=5)"),
    "reversed range allowed": ("if start and end and end < start:", "if False:"),
    "open end is date.min/max, not None": ("start = _date(a) if a else None\n        end = _date(b) if b else None",
                                            "start = _date(a) if a else datetime.date.min\n        end = _date(b) if b else datetime.date.max"),
    "year ends on Dec 30": ("datetime.date(y, 12, 31)", "datetime.date(y, 12, 30)"),
    "spaces not tolerated": ('a, b = (x.strip() for x in t.split("..", 1))', 'a, b = t.split("..", 1)'),
}
