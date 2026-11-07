"""Tests for ledgerly.billing.coupons."""
import datetime
import unittest

from ledgerly.billing.coupons import (
    coupon_due_date,
    coupon_settled,
    format_coupon,
    net_coupon,
    normalize_coupon_ref,
    scaled_coupon,
    split_coupon,
)


class TestBillingCoupons(unittest.TestCase):
    def test_format_coupon(self):
        self.assertEqual(format_coupon(2.5, 'USD'), '2.50 USD')

    def test_coupon_settled(self):
        self.assertEqual(coupon_settled(10.0, 10.0), True)

    def test_scaled_coupon(self):
        self.assertEqual(scaled_coupon(10.0, 1.5, 'USD'), 15.0)

    def test_split_coupon(self):
        self.assertEqual(split_coupon(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_net_coupon(self):
        self.assertEqual(net_coupon(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_coupon_ref(self):
        self.assertEqual(normalize_coupon_ref("  ab_12 cd "), "AB-12-CD")

    def test_coupon_due_date(self):
        self.assertEqual(coupon_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
