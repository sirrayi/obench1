"""Tests for ledgerly.billing.plans."""
import datetime
import unittest

from ledgerly.billing.plans import (
    accrued_plan,
    format_plan,
    net_plan,
    normalize_plan_ref,
    plan_due_date,
    plan_settled,
    scaled_plan,
)


class TestBillingPlans(unittest.TestCase):
    def test_accrued_plan(self):
        self.assertEqual(accrued_plan(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_plan_settled(self):
        self.assertEqual(plan_settled(10.0, 10.0), True)

    def test_format_plan(self):
        self.assertEqual(format_plan(2.5, 'USD'), '2.50 USD')

    def test_net_plan(self):
        self.assertEqual(net_plan(200.0, 10.0, 'USD'), 180.0)

    def test_scaled_plan(self):
        self.assertEqual(scaled_plan(10.0, 1.5, 'USD'), 15.0)

    def test_normalize_plan_ref(self):
        self.assertEqual(normalize_plan_ref("  ab_12 cd "), "AB-12-CD")

    def test_plan_due_date(self):
        self.assertEqual(plan_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
