"""Tests for ledgerly.reports.aging."""
import datetime
import unittest

from ledgerly.reports.aging import (
    accrued_aging,
    aging_due_date,
    aging_settled,
    net_aging,
    normalize_aging_ref,
    scaled_aging,
    total_aging,
)


class TestReportsAging(unittest.TestCase):
    def test_aging_settled(self):
        self.assertEqual(aging_settled(10.0, 10.0), True)

    def test_scaled_aging(self):
        self.assertEqual(scaled_aging(10.0, 1.5, 'USD'), 15.0)

    def test_net_aging(self):
        self.assertEqual(net_aging(200.0, 10.0, 'USD'), 180.0)

    def test_accrued_aging(self):
        self.assertEqual(accrued_aging(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_total_aging(self):
        self.assertEqual(total_aging([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_normalize_aging_ref(self):
        self.assertEqual(normalize_aging_ref("  ab_12 cd "), "AB-12-CD")

    def test_aging_due_date(self):
        self.assertEqual(aging_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
