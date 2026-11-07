"""Tests for ledgerly.invoices.deposits."""
import datetime
import unittest

from ledgerly.invoices.deposits import (
    accrued_deposit,
    capped_deposit,
    deposit_due_date,
    deposit_exceeds,
    deposit_settled,
    format_deposit,
    normalize_deposit_ref,
)


class TestInvoicesDeposits(unittest.TestCase):
    def test_capped_deposit(self):
        self.assertEqual(capped_deposit(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_deposit_exceeds(self):
        self.assertEqual(deposit_exceeds(10.0, 5.0), True)

    def test_accrued_deposit(self):
        self.assertEqual(accrued_deposit(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_format_deposit(self):
        self.assertEqual(format_deposit(2.5, 'USD'), '2.50 USD')

    def test_deposit_settled(self):
        self.assertEqual(deposit_settled(10.0, 10.0), True)

    def test_normalize_deposit_ref(self):
        self.assertEqual(normalize_deposit_ref("  ab_12 cd "), "AB-12-CD")

    def test_deposit_due_date(self):
        self.assertEqual(deposit_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
