import datetime
import unittest

from daterange import parse_range


class TestRange(unittest.TestCase):
    def test_two_dates(self):
        self.assertEqual(parse_range("2026-10-01..2026-10-31"), (datetime.date(2026, 10, 1), datetime.date(2026, 10, 31)))
