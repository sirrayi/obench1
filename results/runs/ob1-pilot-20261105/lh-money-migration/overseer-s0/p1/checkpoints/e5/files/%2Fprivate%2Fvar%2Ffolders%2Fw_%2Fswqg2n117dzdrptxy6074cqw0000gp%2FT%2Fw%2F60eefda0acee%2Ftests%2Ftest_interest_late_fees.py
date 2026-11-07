"""Tests for ledgerly.interest.late_fees."""
import datetime
import unittest

from ledgerly.interest.late_fees import (
    accrued_late_fee,
    capped_late_fee,
    late_fee_due_date,
    late_fee_exceeds,
    late_fee_settled,
    normalize_late_fee_ref,
    percent_of_late_fee,
)


class TestInterestLateFees(unittest.TestCase):
    def test_percent_of_late_fee(self):
        self.assertEqual(percent_of_late_fee(200.0, 7.5, 'USD'), 15.0)

    def test_late_fee_exceeds(self):
        self.assertEqual(late_fee_exceeds(10.0, 5.0), True)

    def test_late_fee_settled(self):
        self.assertEqual(late_fee_settled(10.0, 10.0), True)

    def test_accrued_late_fee(self):
        self.assertEqual(accrued_late_fee(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_capped_late_fee(self):
        self.assertEqual(capped_late_fee(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_normalize_late_fee_ref(self):
        self.assertEqual(normalize_late_fee_ref("  ab_12 cd "), "AB-12-CD")

    def test_late_fee_due_date(self):
        self.assertEqual(late_fee_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
