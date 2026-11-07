"""Tests for ledgerly.export.json_export."""
import datetime
import unittest

from ledgerly.export.json_export import (
    format_json,
    invoice_json,
    json_due_date,
    normalize_json_ref,
    total_json,
)


class TestExportJsonExport(unittest.TestCase):
    def test_invoice_json(self):
        self.assertEqual(invoice_json([('A-1', 10.0), ('B-2', 2.5)], 'USD'), '{"currency":"USD","lines":[{"sku":"A-1","amount":10.0},{"sku":"B-2","amount":2.5}],"total":12.5}')

    def test_format_json(self):
        self.assertEqual(format_json(2.5, 'USD'), '2.50 USD')

    def test_total_json(self):
        self.assertEqual(total_json([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_normalize_json_ref(self):
        self.assertEqual(normalize_json_ref("  ab_12 cd "), "AB-12-CD")

    def test_json_due_date(self):
        self.assertEqual(json_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
