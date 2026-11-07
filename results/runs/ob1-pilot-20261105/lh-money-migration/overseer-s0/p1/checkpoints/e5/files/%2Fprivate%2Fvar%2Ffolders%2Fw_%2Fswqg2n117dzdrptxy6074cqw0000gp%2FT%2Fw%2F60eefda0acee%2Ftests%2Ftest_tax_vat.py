"""Tests for ledgerly.tax.vat."""
import datetime
import unittest

from ledgerly.tax.vat import (
    capped_vat,
    format_vat,
    normalize_vat_ref,
    split_vat,
    total_vat,
    vat_due_date,
    vat_exceeds,
)


class TestTaxVat(unittest.TestCase):
    def test_format_vat(self):
        self.assertEqual(format_vat(2.5, 'USD'), '2.50 USD')

    def test_capped_vat(self):
        self.assertEqual(capped_vat(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_vat_exceeds(self):
        self.assertEqual(vat_exceeds(10.0, 5.0), True)

    def test_total_vat(self):
        self.assertEqual(total_vat([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_split_vat(self):
        self.assertEqual(split_vat(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_normalize_vat_ref(self):
        self.assertEqual(normalize_vat_ref("  ab_12 cd "), "AB-12-CD")

    def test_vat_due_date(self):
        self.assertEqual(vat_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
