"""Tests for ledgerly.refunds.chargebacks."""
import datetime
import unittest

from ledgerly.refunds.chargebacks import (
    accrued_chargeback,
    chargeback_due_date,
    chargeback_exceeds,
    net_chargeback,
    normalize_chargeback_ref,
    percent_of_chargeback,
    split_chargeback,
)


class TestRefundsChargebacks(unittest.TestCase):
    def test_accrued_chargeback(self):
        self.assertEqual(accrued_chargeback(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_split_chargeback(self):
        self.assertEqual(split_chargeback(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_net_chargeback(self):
        self.assertEqual(net_chargeback(200.0, 10.0, 'USD'), 180.0)

    def test_chargeback_exceeds(self):
        self.assertEqual(chargeback_exceeds(10.0, 5.0), True)

    def test_percent_of_chargeback(self):
        self.assertEqual(percent_of_chargeback(200.0, 7.5, 'USD'), 15.0)

    def test_normalize_chargeback_ref(self):
        self.assertEqual(normalize_chargeback_ref("  ab_12 cd "), "AB-12-CD")

    def test_chargeback_due_date(self):
        self.assertEqual(chargeback_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
