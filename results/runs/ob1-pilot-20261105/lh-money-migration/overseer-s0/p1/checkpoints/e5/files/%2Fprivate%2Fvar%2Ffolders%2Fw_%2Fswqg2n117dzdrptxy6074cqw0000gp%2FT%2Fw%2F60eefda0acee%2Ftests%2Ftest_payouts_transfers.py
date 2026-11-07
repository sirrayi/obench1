"""Tests for ledgerly.payouts.transfers."""
import datetime
import unittest

from ledgerly.payouts.transfers import (
    accrued_transfer,
    normalize_transfer_ref,
    percent_of_transfer,
    scaled_transfer,
    split_transfer,
    transfer_due_date,
    transfer_exceeds,
)


class TestPayoutsTransfers(unittest.TestCase):
    def test_accrued_transfer(self):
        self.assertEqual(accrued_transfer(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_split_transfer(self):
        self.assertEqual(split_transfer(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_percent_of_transfer(self):
        self.assertEqual(percent_of_transfer(200.0, 7.5, 'USD'), 15.0)

    def test_transfer_exceeds(self):
        self.assertEqual(transfer_exceeds(10.0, 5.0), True)

    def test_scaled_transfer(self):
        self.assertEqual(scaled_transfer(10.0, 1.5, 'USD'), 15.0)

    def test_normalize_transfer_ref(self):
        self.assertEqual(normalize_transfer_ref("  ab_12 cd "), "AB-12-CD")

    def test_transfer_due_date(self):
        self.assertEqual(transfer_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
