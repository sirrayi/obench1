"""Tests for ledgerly.interest.loans."""
import datetime
import unittest

from ledgerly.interest.loans import (
    capped_loan,
    loan_due_date,
    loan_exceeds,
    normalize_loan_ref,
    percent_of_loan,
    scaled_loan,
    split_loan,
)


class TestInterestLoans(unittest.TestCase):
    def test_percent_of_loan(self):
        self.assertEqual(percent_of_loan(200.0, 7.5, 'USD'), 15.0)

    def test_capped_loan(self):
        self.assertEqual(capped_loan(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_scaled_loan(self):
        self.assertEqual(scaled_loan(10.0, 1.5, 'USD'), 15.0)

    def test_loan_exceeds(self):
        self.assertEqual(loan_exceeds(10.0, 5.0), True)

    def test_split_loan(self):
        self.assertEqual(split_loan(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_normalize_loan_ref(self):
        self.assertEqual(normalize_loan_ref("  ab_12 cd "), "AB-12-CD")

    def test_loan_due_date(self):
        self.assertEqual(loan_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
