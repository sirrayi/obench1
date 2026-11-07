"""Tests for ledgerly.fx.quotes."""
import datetime
import unittest

from ledgerly.fx.quotes import (
    accrued_quote,
    convert_quote,
    normalize_quote_ref,
    quote_due_date,
    quote_exceeds,
    quote_quote,
    split_quote,
)


class TestFxQuotes(unittest.TestCase):
    def test_convert_quote(self):
        self.assertEqual(convert_quote(100.0, 'USD', 'EUR'), 92.13)

    def test_quote_quote(self):
        self.assertEqual(quote_quote(100.0, 'USD', 'EUR', 50), 91.67)

    def test_quote_exceeds(self):
        self.assertEqual(quote_exceeds(10.0, 5.0), True)

    def test_accrued_quote(self):
        self.assertEqual(accrued_quote(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_split_quote(self):
        self.assertEqual(split_quote(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_normalize_quote_ref(self):
        self.assertEqual(normalize_quote_ref("  ab_12 cd "), "AB-12-CD")

    def test_quote_due_date(self):
        self.assertEqual(quote_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
