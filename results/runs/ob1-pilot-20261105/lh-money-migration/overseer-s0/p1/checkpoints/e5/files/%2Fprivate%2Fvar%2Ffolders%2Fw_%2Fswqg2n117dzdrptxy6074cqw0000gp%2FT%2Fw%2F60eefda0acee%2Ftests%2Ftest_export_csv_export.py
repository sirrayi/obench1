"""Tests for ledgerly.export.csv_export."""
import datetime
import unittest

from ledgerly.export.csv_export import (
    csv_due_date,
    format_csv,
    ledger_csv,
    normalize_csv_ref,
    total_csv,
)


class TestExportCsvExport(unittest.TestCase):
    def test_ledger_csv(self):
        self.assertEqual(ledger_csv([('2026-10-01', 'rent', 1200.0)], 'USD'), 'date,memo,amount,currency\n2026-10-01,rent,1200.00,USD\n')

    def test_format_csv(self):
        self.assertEqual(format_csv(2.5, 'USD'), '2.50 USD')

    def test_total_csv(self):
        self.assertEqual(total_csv([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_normalize_csv_ref(self):
        self.assertEqual(normalize_csv_ref("  ab_12 cd "), "AB-12-CD")

    def test_csv_due_date(self):
        self.assertEqual(csv_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
