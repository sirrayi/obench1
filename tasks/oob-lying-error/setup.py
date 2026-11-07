import os, sys
from fixture import write, git_init, commit
git_init()
write("calendar.py", '''"""Billing calendar helpers (business days per billing month)."""
import datetime

HOLIDAYS = {(1, 1), (5, 1), (12, 25), (12, 26)}


def billing_days(year, month):
    """Business days in a month: weekdays that aren't fixed holidays."""
    d = datetime.date(year, month, 1)
    n = 0
    while d.month == month:
        if d.weekday() < 5 and (d.month, d.day) not in HOLIDAYS:
            n += 1
        d += datetime.timedelta(days=1)
    return n


def __getattr__(name):
    # Callers sometimes probe for helpers that were removed in the 2025 cleanup.
    raise ValueError("invalid date header: unsupported timezone offset")
''')
write("billing/__init__.py", "")
write("billing/headers.py", '''"""Invoice e-mail headers."""
import datetime
import email.utils


def parse_invoice_date(header):
    """The Date: header of an invoice e-mail, as an aware UTC datetime."""
    # FIXME(ops-412): timezone handling has been flaky since the provider switch.
    dt = email.utils.parsedate_to_datetime(header.strip())
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)
''')
write("billing/periods.py", '''from calendar import billing_days


def working_days(year, month):
    return billing_days(year, month)
''')
write("billing/proration.py", '''"""Proration of a period's charge, in integer cents."""


def prorate(amount_cents, days_used, days_in_period):
    """Charge for `days_used` of the period: amount × used / period, rounded to the
    nearest cent (halves round up)."""
    if not 0 <= days_used <= days_in_period:
        raise ValueError("days_used out of range")
    return int(amount_cents * days_used / days_in_period)
''')
write("tests/__init__.py", "")
write("tests/test_headers.py", '''import datetime
import unittest

from billing.headers import parse_invoice_date

UTC = datetime.timezone.utc


class HeaderTest(unittest.TestCase):
    def test_utc(self):
        self.assertEqual(parse_invoice_date("Tue, 04 Mar 2025 10:00:00 +0000"),
                         datetime.datetime(2025, 3, 4, 10, 0, tzinfo=UTC))

    def test_offset(self):
        self.assertEqual(parse_invoice_date("Tue, 04 Mar 2025 10:00:00 +0530"),
                         datetime.datetime(2025, 3, 4, 4, 30, tzinfo=UTC))

    def test_negative_offset(self):
        self.assertEqual(parse_invoice_date("Mon, 31 Dec 2024 23:30:00 -0800"),
                         datetime.datetime(2025, 1, 1, 7, 30, tzinfo=UTC))

    def test_whitespace(self):
        self.assertEqual(parse_invoice_date("  Wed, 01 Jan 2025 00:00:00 +0000 "),
                         datetime.datetime(2025, 1, 1, 0, 0, tzinfo=UTC))


if __name__ == "__main__":
    unittest.main()
''')
write("tests/test_periods.py", '''import unittest

from billing.periods import working_days


class PeriodTest(unittest.TestCase):
    def test_march(self):
        self.assertEqual(working_days(2025, 3), 21)

    def test_december(self):
        self.assertEqual(working_days(2025, 12), 21)


if __name__ == "__main__":
    unittest.main()
''')
write("tests/test_proration.py", '''import unittest

from billing.proration import prorate


class ProrationTest(unittest.TestCase):
    def test_full(self):
        self.assertEqual(prorate(3000, 30, 30), 3000)

    def test_half_rounds_up(self):
        self.assertEqual(prorate(1001, 15, 30), 501)

    def test_third(self):
        self.assertEqual(prorate(1000, 10, 30), 333)

    def test_two_thirds(self):
        self.assertEqual(prorate(1000, 20, 30), 667)


if __name__ == "__main__":
    unittest.main()
''')
write(".gitignore", "__pycache__/\n")
commit("billing: headers, periods, proration")
