"""Tests for ledgerly.invoices.subtotals."""
import datetime
import unittest

from ledgerly.invoices.subtotals import (
    net_subtotal,
    normalize_subtotal_ref,
    scaled_subtotal,
    split_subtotal,
    subtotal_due_date,
    subtotal_exceeds,
    total_subtotal,
)


class TestInvoicesSubtotals(unittest.TestCase):
    def test_net_subtotal(self):
        self.assertEqual(net_subtotal(200.0, 10.0, 'USD'), 180.0)

    def test_split_subtotal(self):
        self.assertEqual(split_subtotal(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_subtotal_exceeds(self):
        self.assertEqual(subtotal_exceeds(10.0, 5.0), True)

    def test_total_subtotal(self):
        self.assertEqual(total_subtotal([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_scaled_subtotal(self):
        self.assertEqual(scaled_subtotal(10.0, 1.5, 'USD'), 15.0)

    def test_normalize_subtotal_ref(self):
        self.assertEqual(normalize_subtotal_ref("  ab_12 cd "), "AB-12-CD")

    def test_subtotal_due_date(self):
        self.assertEqual(subtotal_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
