"""Tests for ledgerly.fx.revaluation."""
import datetime
import unittest

from ledgerly.fx.revaluation import (
    accrued_revaluation,
    convert_revaluation,
    net_revaluation,
    normalize_revaluation_ref,
    quote_revaluation,
    revaluation_due_date,
    split_revaluation,
)


class TestFxRevaluation(unittest.TestCase):
    def test_convert_revaluation(self):
        self.assertEqual(convert_revaluation(100.0, 'USD', 'EUR'), 92.13)

    def test_quote_revaluation(self):
        self.assertEqual(quote_revaluation(100.0, 'USD', 'EUR', 50), 91.67)

    def test_net_revaluation(self):
        self.assertEqual(net_revaluation(200.0, 10.0, 'USD'), 180.0)

    def test_accrued_revaluation(self):
        self.assertEqual(accrued_revaluation(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_split_revaluation(self):
        self.assertEqual(split_revaluation(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_normalize_revaluation_ref(self):
        self.assertEqual(normalize_revaluation_ref("  ab_12 cd "), "AB-12-CD")

    def test_revaluation_due_date(self):
        self.assertEqual(revaluation_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
