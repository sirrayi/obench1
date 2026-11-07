"""Tests for ledgerly.payouts.instant."""
import datetime
import unittest

from ledgerly.payouts.instant import (
    format_instant_payout,
    instant_payout_due_date,
    instant_payout_exceeds,
    normalize_instant_payout_ref,
    percent_of_instant_payout,
    split_instant_payout,
)


class TestPayoutsInstant(unittest.TestCase):
    def test_percent_of_instant_payout(self):
        self.assertEqual(percent_of_instant_payout(200.0, 7.5, 'USD'), 15.0)

    def test_split_instant_payout(self):
        self.assertEqual(split_instant_payout(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_format_instant_payout(self):
        self.assertEqual(format_instant_payout(2.5, 'USD'), '2.50 USD')

    def test_instant_payout_exceeds(self):
        self.assertEqual(instant_payout_exceeds(10.0, 5.0), True)

    def test_normalize_instant_payout_ref(self):
        self.assertEqual(normalize_instant_payout_ref("  ab_12 cd "), "AB-12-CD")

    def test_instant_payout_due_date(self):
        self.assertEqual(instant_payout_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
