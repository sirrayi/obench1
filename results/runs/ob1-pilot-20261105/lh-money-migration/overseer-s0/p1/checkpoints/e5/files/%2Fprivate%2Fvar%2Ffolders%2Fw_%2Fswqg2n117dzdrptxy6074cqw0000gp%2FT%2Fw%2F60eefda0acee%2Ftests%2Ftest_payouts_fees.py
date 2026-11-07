"""Tests for ledgerly.payouts.fees."""
import datetime
import unittest

from ledgerly.payouts.fees import (
    capped_fee,
    fee_due_date,
    fee_settled,
    net_fee,
    normalize_fee_ref,
    scaled_fee,
    split_fee,
)


class TestPayoutsFees(unittest.TestCase):
    def test_fee_settled(self):
        self.assertEqual(fee_settled(10.0, 10.0), True)

    def test_split_fee(self):
        self.assertEqual(split_fee(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_capped_fee(self):
        self.assertEqual(capped_fee(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_scaled_fee(self):
        self.assertEqual(scaled_fee(10.0, 1.5, 'USD'), 15.0)

    def test_net_fee(self):
        self.assertEqual(net_fee(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_fee_ref(self):
        self.assertEqual(normalize_fee_ref("  ab_12 cd "), "AB-12-CD")

    def test_fee_due_date(self):
        self.assertEqual(fee_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
