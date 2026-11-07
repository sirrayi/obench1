"""Tests for ledgerly.interest.savings."""
import datetime
import unittest

from ledgerly.interest.savings import (
    accrued_savings,
    capped_savings,
    normalize_savings_ref,
    percent_of_savings,
    savings_due_date,
    savings_exceeds,
    split_savings,
)


class TestInterestSavings(unittest.TestCase):
    def test_capped_savings(self):
        self.assertEqual(capped_savings(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_percent_of_savings(self):
        self.assertEqual(percent_of_savings(200.0, 7.5, 'USD'), 15.0)

    def test_savings_exceeds(self):
        self.assertEqual(savings_exceeds(10.0, 5.0), True)

    def test_split_savings(self):
        self.assertEqual(split_savings(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_accrued_savings(self):
        self.assertEqual(accrued_savings(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_normalize_savings_ref(self):
        self.assertEqual(normalize_savings_ref("  ab_12 cd "), "AB-12-CD")

    def test_savings_due_date(self):
        self.assertEqual(savings_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
