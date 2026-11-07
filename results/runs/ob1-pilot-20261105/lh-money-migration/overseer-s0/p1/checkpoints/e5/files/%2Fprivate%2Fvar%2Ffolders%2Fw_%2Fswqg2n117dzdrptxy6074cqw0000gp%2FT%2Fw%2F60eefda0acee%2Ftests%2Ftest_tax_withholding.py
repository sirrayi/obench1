"""Tests for ledgerly.tax.withholding."""
import datetime
import unittest

from ledgerly.tax.withholding import (
    net_withholding,
    normalize_withholding_ref,
    percent_of_withholding,
    scaled_withholding,
    split_withholding,
    withholding_due_date,
    withholding_exceeds,
)


class TestTaxWithholding(unittest.TestCase):
    def test_net_withholding(self):
        self.assertEqual(net_withholding(200.0, 10.0, 'USD'), 180.0)

    def test_scaled_withholding(self):
        self.assertEqual(scaled_withholding(10.0, 1.5, 'USD'), 15.0)

    def test_withholding_exceeds(self):
        self.assertEqual(withholding_exceeds(10.0, 5.0), True)

    def test_split_withholding(self):
        self.assertEqual(split_withholding(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_percent_of_withholding(self):
        self.assertEqual(percent_of_withholding(200.0, 7.5, 'USD'), 15.0)

    def test_normalize_withholding_ref(self):
        self.assertEqual(normalize_withholding_ref("  ab_12 cd "), "AB-12-CD")

    def test_withholding_due_date(self):
        self.assertEqual(withholding_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
