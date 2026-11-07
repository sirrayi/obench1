"""Tests for ledgerly.interest.accrual."""
import datetime
import unittest

from ledgerly.interest.accrual import (
    accrual_due_date,
    accrual_settled,
    capped_accrual,
    normalize_accrual_ref,
    percent_of_accrual,
    scaled_accrual,
    total_accrual,
)


class TestInterestAccrual(unittest.TestCase):
    def test_total_accrual(self):
        self.assertEqual(total_accrual([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_percent_of_accrual(self):
        self.assertEqual(percent_of_accrual(200.0, 7.5, 'USD'), 15.0)

    def test_capped_accrual(self):
        self.assertEqual(capped_accrual(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_scaled_accrual(self):
        self.assertEqual(scaled_accrual(10.0, 1.5, 'USD'), 15.0)

    def test_accrual_settled(self):
        self.assertEqual(accrual_settled(10.0, 10.0), True)

    def test_normalize_accrual_ref(self):
        self.assertEqual(normalize_accrual_ref("  ab_12 cd "), "AB-12-CD")

    def test_accrual_due_date(self):
        self.assertEqual(accrual_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
