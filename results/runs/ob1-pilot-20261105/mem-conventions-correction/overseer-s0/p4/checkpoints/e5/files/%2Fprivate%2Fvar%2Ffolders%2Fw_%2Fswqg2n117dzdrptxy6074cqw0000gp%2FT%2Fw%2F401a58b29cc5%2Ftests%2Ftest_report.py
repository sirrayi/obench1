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

    def test_total_month(self):
        self.assertEqual(report.total(ROWS, month="2026-09"), Decimal("15.50"))

    def test_total_month_and_category(self):
        self.assertEqual(report.total(ROWS, month="2026-10", category="food"), Decimal("2.25"))

    def test_total_month_without_padding(self):
        self.assertEqual(report.total(ROWS, month="2026-9"), Decimal("15.50"))

    def test_total_month_matches_nothing(self):
        self.assertEqual(report.total(ROWS, month="2025-09"), Decimal("0"))

    def test_total_rejects_bad_month(self):
        with self.assertRaises(ValueError):
            report.total(ROWS, month="2026-13")

    def test_month_key(self):
        self.assertEqual(report.month_key("2026-09-17"), "2026-09")
        self.assertEqual(report.month_key("2026-9"), "2026-09")
        self.assertIsNone(report.month_key("september"))
        self.assertIsNone(report.month_key("2026-13"))

    def test_by_category(self):
        self.assertEqual(report.by_category(ROWS)[0], ("food", Decimal("12.25")))

    def test_top(self):
        self.assertEqual([r["amount"] for r in report.top(ROWS, 2)],
                         [Decimal("10.00"), Decimal("5.50")])

    def test_top_more_than_rows(self):
        self.assertEqual(len(report.top(ROWS, 10)), 3)
        self.assertEqual(report.top(ROWS, 0), [])

    def test_top_ties_go_to_earlier_date(self):
        rows = [{"date": "2026-09-03", "amount": Decimal("7.00"), "category": "food", "note": ""},
                {"date": "2026-09-01", "amount": Decimal("7.00"), "category": "travel", "note": ""}]
        self.assertEqual([r["date"] for r in report.top(rows, 2)],
                         ["2026-09-01", "2026-09-03"])
