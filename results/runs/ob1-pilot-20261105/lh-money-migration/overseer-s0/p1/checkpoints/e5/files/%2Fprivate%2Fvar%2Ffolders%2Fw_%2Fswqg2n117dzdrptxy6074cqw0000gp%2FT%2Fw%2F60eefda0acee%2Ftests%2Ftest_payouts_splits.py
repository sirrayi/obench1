"""Tests for ledgerly.payouts.splits."""
import datetime
import unittest

from ledgerly.payouts.splits import (
    accrued_split,
    format_split,
    normalize_split_ref,
    scaled_split,
    split_due_date,
    split_exceeds,
    total_split,
)


class TestPayoutsSplits(unittest.TestCase):
    def test_scaled_split(self):
        self.assertEqual(scaled_split(10.0, 1.5, 'USD'), 15.0)

    def test_accrued_split(self):
        self.assertEqual(accrued_split(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_split_exceeds(self):
        self.assertEqual(split_exceeds(10.0, 5.0), True)

    def test_total_split(self):
        self.assertEqual(total_split([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_format_split(self):
        self.assertEqual(format_split(2.5, 'USD'), '2.50 USD')

    def test_normalize_split_ref(self):
        self.assertEqual(normalize_split_ref("  ab_12 cd "), "AB-12-CD")

    def test_split_due_date(self):
        self.assertEqual(split_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
