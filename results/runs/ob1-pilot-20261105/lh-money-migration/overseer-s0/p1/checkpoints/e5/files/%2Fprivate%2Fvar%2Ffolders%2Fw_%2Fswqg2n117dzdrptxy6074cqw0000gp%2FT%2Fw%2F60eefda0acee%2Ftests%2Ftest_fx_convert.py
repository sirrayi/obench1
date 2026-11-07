"""Tests for ledgerly.fx.convert."""
import datetime
import unittest

from ledgerly.fx.convert import (
    conversion_due_date,
    convert_conversion,
    convert_float,
    net_conversion,
    normalize_conversion_ref,
    quote_conversion,
    scaled_conversion,
    total_conversion,
)


class TestFxConvert(unittest.TestCase):
    def test_convert_conversion(self):
        self.assertEqual(convert_conversion(100.0, 'USD', 'EUR'), 92.13)

    def test_quote_conversion(self):
        self.assertEqual(quote_conversion(100.0, 'USD', 'EUR', 50), 91.67)

    def test_net_conversion(self):
        self.assertEqual(net_conversion(200.0, 10.0, 'USD'), 180.0)

    def test_scaled_conversion(self):
        self.assertEqual(scaled_conversion(10.0, 1.5, 'USD'), 15.0)

    def test_total_conversion(self):
        self.assertEqual(total_conversion([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_convert_float(self):
        self.assertEqual(convert_float(100.0, 'USD', 'EUR'), 92.13)

    def test_normalize_conversion_ref(self):
        self.assertEqual(normalize_conversion_ref("  ab_12 cd "), "AB-12-CD")

    def test_conversion_due_date(self):
        self.assertEqual(conversion_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
