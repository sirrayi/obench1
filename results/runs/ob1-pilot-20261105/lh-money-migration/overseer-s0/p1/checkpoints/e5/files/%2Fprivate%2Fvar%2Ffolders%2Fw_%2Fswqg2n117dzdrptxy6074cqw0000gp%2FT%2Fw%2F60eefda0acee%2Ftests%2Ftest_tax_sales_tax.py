"""Tests for ledgerly.tax.sales_tax."""
import datetime
import unittest

from ledgerly.tax.sales_tax import (
    accrued_sales_tax,
    format_sales_tax,
    net_sales_tax,
    normalize_sales_tax_ref,
    sales_tax_due_date,
    sales_tax_settled,
    scaled_sales_tax,
)


class TestTaxSalesTax(unittest.TestCase):
    def test_sales_tax_settled(self):
        self.assertEqual(sales_tax_settled(10.0, 10.0), True)

    def test_net_sales_tax(self):
        self.assertEqual(net_sales_tax(200.0, 10.0, 'USD'), 180.0)

    def test_format_sales_tax(self):
        self.assertEqual(format_sales_tax(2.5, 'USD'), '2.50 USD')

    def test_accrued_sales_tax(self):
        self.assertEqual(accrued_sales_tax(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_scaled_sales_tax(self):
        self.assertEqual(scaled_sales_tax(10.0, 1.5, 'USD'), 15.0)

    def test_normalize_sales_tax_ref(self):
        self.assertEqual(normalize_sales_tax_ref("  ab_12 cd "), "AB-12-CD")

    def test_sales_tax_due_date(self):
        self.assertEqual(sales_tax_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
