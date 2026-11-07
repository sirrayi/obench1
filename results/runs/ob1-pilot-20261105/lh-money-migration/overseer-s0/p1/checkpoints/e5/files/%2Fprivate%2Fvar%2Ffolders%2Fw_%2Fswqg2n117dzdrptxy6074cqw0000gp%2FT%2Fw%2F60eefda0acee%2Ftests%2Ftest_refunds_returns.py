"""Tests for ledgerly.refunds.returns."""
import datetime
import unittest

from ledgerly.refunds.returns import (
    accrued_return,
    format_return,
    net_return,
    normalize_return_ref,
    return_due_date,
    scaled_return,
    total_return,
)


class TestRefundsReturns(unittest.TestCase):
    def test_scaled_return(self):
        self.assertEqual(scaled_return(10.0, 1.5, 'USD'), 15.0)

    def test_accrued_return(self):
        self.assertEqual(accrued_return(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_format_return(self):
        self.assertEqual(format_return(2.5, 'USD'), '2.50 USD')

    def test_net_return(self):
        self.assertEqual(net_return(200.0, 10.0, 'USD'), 180.0)

    def test_total_return(self):
        self.assertEqual(total_return([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_normalize_return_ref(self):
        self.assertEqual(normalize_return_ref("  ab_12 cd "), "AB-12-CD")

    def test_return_due_date(self):
        self.assertEqual(return_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
