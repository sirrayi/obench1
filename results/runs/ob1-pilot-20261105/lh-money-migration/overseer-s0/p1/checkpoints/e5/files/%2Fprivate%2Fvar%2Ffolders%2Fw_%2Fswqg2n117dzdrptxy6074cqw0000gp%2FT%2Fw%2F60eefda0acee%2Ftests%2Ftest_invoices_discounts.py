"""Tests for ledgerly.invoices.discounts."""
import datetime
import unittest

from ledgerly.invoices.discounts import (
    capped_discount,
    discount_due_date,
    discount_exceeds,
    discount_settled,
    normalize_discount_ref,
    scaled_discount,
    split_discount,
)


class TestInvoicesDiscounts(unittest.TestCase):
    def test_scaled_discount(self):
        self.assertEqual(scaled_discount(10.0, 1.5, 'USD'), 15.0)

    def test_capped_discount(self):
        self.assertEqual(capped_discount(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_discount_exceeds(self):
        self.assertEqual(discount_exceeds(10.0, 5.0), True)

    def test_split_discount(self):
        self.assertEqual(split_discount(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_discount_settled(self):
        self.assertEqual(discount_settled(10.0, 10.0), True)

    def test_normalize_discount_ref(self):
        self.assertEqual(normalize_discount_ref("  ab_12 cd "), "AB-12-CD")

    def test_discount_due_date(self):
        self.assertEqual(discount_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
