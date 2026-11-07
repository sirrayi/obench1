"""Tests for ledgerly.invoices.credits."""
import datetime
import unittest

from ledgerly.invoices.credits import (
    credit_due_date,
    credit_exceeds,
    credit_settled,
    format_credit,
    net_credit,
    normalize_credit_ref,
    percent_of_credit,
)


class TestInvoicesCredits(unittest.TestCase):
    def test_percent_of_credit(self):
        self.assertEqual(percent_of_credit(200.0, 7.5, 'USD'), 15.0)

    def test_credit_exceeds(self):
        self.assertEqual(credit_exceeds(10.0, 5.0), True)

    def test_credit_settled(self):
        self.assertEqual(credit_settled(10.0, 10.0), True)

    def test_format_credit(self):
        self.assertEqual(format_credit(2.5, 'USD'), '2.50 USD')

    def test_net_credit(self):
        self.assertEqual(net_credit(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_credit_ref(self):
        self.assertEqual(normalize_credit_ref("  ab_12 cd "), "AB-12-CD")

    def test_credit_due_date(self):
        self.assertEqual(credit_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
