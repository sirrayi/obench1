"""Tests for ledgerly.billing.proration."""
import datetime
import unittest

from ledgerly.billing.proration import (
    format_prorated,
    net_prorated,
    normalize_prorated_ref,
    percent_of_prorated,
    prorated_due_date,
    prorated_settled,
    total_prorated,
)


class TestBillingProration(unittest.TestCase):
    def test_format_prorated(self):
        self.assertEqual(format_prorated(2.5, 'USD'), '2.50 USD')

    def test_prorated_settled(self):
        self.assertEqual(prorated_settled(10.0, 10.0), True)

    def test_percent_of_prorated(self):
        self.assertEqual(percent_of_prorated(200.0, 7.5, 'USD'), 15.0)

    def test_total_prorated(self):
        self.assertEqual(total_prorated([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_net_prorated(self):
        self.assertEqual(net_prorated(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_prorated_ref(self):
        self.assertEqual(normalize_prorated_ref("  ab_12 cd "), "AB-12-CD")

    def test_prorated_due_date(self):
        self.assertEqual(prorated_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
