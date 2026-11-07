"""Tests for ledgerly.refunds.cancellations."""
import datetime
import unittest

from ledgerly.refunds.cancellations import (
    accrued_cancellation,
    cancellation_due_date,
    cancellation_exceeds,
    cancellation_settled,
    format_cancellation,
    normalize_cancellation_ref,
    percent_of_cancellation,
)


class TestRefundsCancellations(unittest.TestCase):
    def test_cancellation_exceeds(self):
        self.assertEqual(cancellation_exceeds(10.0, 5.0), True)

    def test_cancellation_settled(self):
        self.assertEqual(cancellation_settled(10.0, 10.0), True)

    def test_accrued_cancellation(self):
        self.assertEqual(accrued_cancellation(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_format_cancellation(self):
        self.assertEqual(format_cancellation(2.5, 'USD'), '2.50 USD')

    def test_percent_of_cancellation(self):
        self.assertEqual(percent_of_cancellation(200.0, 7.5, 'USD'), 15.0)

    def test_normalize_cancellation_ref(self):
        self.assertEqual(normalize_cancellation_ref("  ab_12 cd "), "AB-12-CD")

    def test_cancellation_due_date(self):
        self.assertEqual(cancellation_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
