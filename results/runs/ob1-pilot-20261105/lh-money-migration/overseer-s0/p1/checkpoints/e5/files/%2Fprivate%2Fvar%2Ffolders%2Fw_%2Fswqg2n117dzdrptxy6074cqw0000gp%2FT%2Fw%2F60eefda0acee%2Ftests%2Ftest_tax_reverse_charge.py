"""Tests for ledgerly.tax.reverse_charge."""
import datetime
import unittest

from ledgerly.tax.reverse_charge import (
    accrued_reverse_charge,
    capped_reverse_charge,
    normalize_reverse_charge_ref,
    reverse_charge_due_date,
    reverse_charge_exceeds,
    reverse_charge_settled,
    split_reverse_charge,
)


class TestTaxReverseCharge(unittest.TestCase):
    def test_accrued_reverse_charge(self):
        self.assertEqual(accrued_reverse_charge(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_reverse_charge_settled(self):
        self.assertEqual(reverse_charge_settled(10.0, 10.0), True)

    def test_capped_reverse_charge(self):
        self.assertEqual(capped_reverse_charge(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_split_reverse_charge(self):
        self.assertEqual(split_reverse_charge(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_reverse_charge_exceeds(self):
        self.assertEqual(reverse_charge_exceeds(10.0, 5.0), True)

    def test_normalize_reverse_charge_ref(self):
        self.assertEqual(normalize_reverse_charge_ref("  ab_12 cd "), "AB-12-CD")

    def test_reverse_charge_due_date(self):
        self.assertEqual(reverse_charge_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
