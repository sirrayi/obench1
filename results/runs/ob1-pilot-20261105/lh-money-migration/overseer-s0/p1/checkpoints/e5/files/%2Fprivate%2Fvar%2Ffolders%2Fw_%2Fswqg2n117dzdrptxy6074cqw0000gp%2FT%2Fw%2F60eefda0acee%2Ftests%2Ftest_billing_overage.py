"""Tests for ledgerly.billing.overage."""
import datetime
import unittest

from ledgerly.billing.overage import (
    normalize_overage_ref,
    overage_due_date,
    overage_exceeds,
    overage_settled,
    percent_of_overage,
    split_overage,
    total_overage,
)


class TestBillingOverage(unittest.TestCase):
    def test_overage_settled(self):
        self.assertEqual(overage_settled(10.0, 10.0), True)

    def test_split_overage(self):
        self.assertEqual(split_overage(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_percent_of_overage(self):
        self.assertEqual(percent_of_overage(200.0, 7.5, 'USD'), 15.0)

    def test_overage_exceeds(self):
        self.assertEqual(overage_exceeds(10.0, 5.0), True)

    def test_total_overage(self):
        self.assertEqual(total_overage([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_normalize_overage_ref(self):
        self.assertEqual(normalize_overage_ref("  ab_12 cd "), "AB-12-CD")

    def test_overage_due_date(self):
        self.assertEqual(overage_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
