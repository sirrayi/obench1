"""Tests for ledgerly.fx.spreads."""
import datetime
import unittest

from ledgerly.fx.spreads import (
    capped_spread,
    convert_spread,
    format_spread,
    normalize_spread_ref,
    quote_spread,
    scaled_spread,
    spread_due_date,
)


class TestFxSpreads(unittest.TestCase):
    def test_convert_spread(self):
        self.assertEqual(convert_spread(100.0, 'USD', 'EUR'), 92.13)

    def test_quote_spread(self):
        self.assertEqual(quote_spread(100.0, 'USD', 'EUR', 50), 91.67)

    def test_scaled_spread(self):
        self.assertEqual(scaled_spread(10.0, 1.5, 'USD'), 15.0)

    def test_capped_spread(self):
        self.assertEqual(capped_spread(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_format_spread(self):
        self.assertEqual(format_spread(2.5, 'USD'), '2.50 USD')

    def test_normalize_spread_ref(self):
        self.assertEqual(normalize_spread_ref("  ab_12 cd "), "AB-12-CD")

    def test_spread_due_date(self):
        self.assertEqual(spread_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
