import unittest
from decimal import Decimal

from tally import report

ROWS = [{"date": "2026-09-01", "amount": Decimal("10.00"), "category": "food", "note": ""},
        {"date": "2026-09-02", "amount": Decimal("5.50"), "category": "travel", "note": ""},
        {"date": "2026-10-01", "amount": Decimal("2.25"), "category": "food", "note": ""}]


class TestReport(unittest.TestCase):
    def test_total(self):
        self.assertEqual(report.total(ROWS), Decimal("17.75"))

    def test_total_category(self):
        self.assertEqual(report.total(ROWS, category="food"), Decimal("12.25"))

    def test_by_category(self):
        self.assertEqual(report.by_category(ROWS)[0], ("food", Decimal("12.25")))
