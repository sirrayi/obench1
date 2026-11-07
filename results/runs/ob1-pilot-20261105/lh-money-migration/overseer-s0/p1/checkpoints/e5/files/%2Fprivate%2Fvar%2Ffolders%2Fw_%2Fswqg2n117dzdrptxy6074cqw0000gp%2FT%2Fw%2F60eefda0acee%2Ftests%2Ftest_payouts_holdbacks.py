"""Tests for ledgerly.payouts.holdbacks."""
import datetime
import unittest

from ledgerly.payouts.holdbacks import (
    accrued_holdback,
    capped_holdback,
    format_holdback,
    holdback_due_date,
    net_holdback,
    normalize_holdback_ref,
    scaled_holdback,
)


class TestPayoutsHoldbacks(unittest.TestCase):
    def test_capped_holdback(self):
        self.assertEqual(capped_holdback(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_scaled_holdback(self):
        self.assertEqual(scaled_holdback(10.0, 1.5, 'USD'), 15.0)

    def test_format_holdback(self):
        self.assertEqual(format_holdback(2.5, 'USD'), '2.50 USD')

    def test_net_holdback(self):
        self.assertEqual(net_holdback(200.0, 10.0, 'USD'), 180.0)

    def test_accrued_holdback(self):
        self.assertEqual(accrued_holdback(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_normalize_holdback_ref(self):
        self.assertEqual(normalize_holdback_ref("  ab_12 cd "), "AB-12-CD")

    def test_holdback_due_date(self):
        self.assertEqual(holdback_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
