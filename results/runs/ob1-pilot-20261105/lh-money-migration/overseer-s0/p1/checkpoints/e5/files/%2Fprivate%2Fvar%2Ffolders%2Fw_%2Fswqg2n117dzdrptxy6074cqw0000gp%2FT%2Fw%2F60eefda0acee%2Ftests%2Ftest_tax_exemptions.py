"""Tests for ledgerly.tax.exemptions."""
import datetime
import unittest

from ledgerly.tax.exemptions import (
    accrued_exemption,
    exemption_due_date,
    exemption_exceeds,
    normalize_exemption_ref,
    scaled_exemption,
    split_exemption,
    total_exemption,
)


class TestTaxExemptions(unittest.TestCase):
    def test_scaled_exemption(self):
        self.assertEqual(scaled_exemption(10.0, 1.5, 'USD'), 15.0)

    def test_accrued_exemption(self):
        self.assertEqual(accrued_exemption(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_total_exemption(self):
        self.assertEqual(total_exemption([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_split_exemption(self):
        self.assertEqual(split_exemption(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_exemption_exceeds(self):
        self.assertEqual(exemption_exceeds(10.0, 5.0), True)

    def test_normalize_exemption_ref(self):
        self.assertEqual(normalize_exemption_ref("  ab_12 cd "), "AB-12-CD")

    def test_exemption_due_date(self):
        self.assertEqual(exemption_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
