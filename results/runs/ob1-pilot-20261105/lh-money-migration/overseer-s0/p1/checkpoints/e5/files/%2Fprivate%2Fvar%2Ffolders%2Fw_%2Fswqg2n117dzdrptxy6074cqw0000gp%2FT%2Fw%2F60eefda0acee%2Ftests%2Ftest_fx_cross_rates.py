"""Tests for ledgerly.fx.cross_rates."""
import datetime
import unittest

from ledgerly.fx.cross_rates import (
    accrued_cross,
    convert_cross,
    cross_due_date,
    net_cross,
    normalize_cross_ref,
    percent_of_cross,
    quote_cross,
)


class TestFxCrossRates(unittest.TestCase):
    def test_convert_cross(self):
        self.assertEqual(convert_cross(100.0, 'USD', 'EUR'), 92.13)

    def test_quote_cross(self):
        self.assertEqual(quote_cross(100.0, 'USD', 'EUR', 50), 91.67)

    def test_accrued_cross(self):
        self.assertEqual(accrued_cross(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_net_cross(self):
        self.assertEqual(net_cross(200.0, 10.0, 'USD'), 180.0)

    def test_percent_of_cross(self):
        self.assertEqual(percent_of_cross(200.0, 7.5, 'USD'), 15.0)

    def test_normalize_cross_ref(self):
        self.assertEqual(normalize_cross_ref("  ab_12 cd "), "AB-12-CD")

    def test_cross_due_date(self):
        self.assertEqual(cross_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
