"""Tests for ledgerly.payouts.commissions."""
import datetime
import unittest

from ledgerly.payouts.commissions import (
    accrued_commission,
    capped_commission,
    commission_due_date,
    commission_settled,
    format_commission,
    normalize_commission_ref,
    total_commission,
)


class TestPayoutsCommissions(unittest.TestCase):
    def test_capped_commission(self):
        self.assertEqual(capped_commission(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_total_commission(self):
        self.assertEqual(total_commission([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_format_commission(self):
        self.assertEqual(format_commission(2.5, 'USD'), '2.50 USD')

    def test_accrued_commission(self):
        self.assertEqual(accrued_commission(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_commission_settled(self):
        self.assertEqual(commission_settled(10.0, 10.0), True)

    def test_normalize_commission_ref(self):
        self.assertEqual(normalize_commission_ref("  ab_12 cd "), "AB-12-CD")

    def test_commission_due_date(self):
        self.assertEqual(commission_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
