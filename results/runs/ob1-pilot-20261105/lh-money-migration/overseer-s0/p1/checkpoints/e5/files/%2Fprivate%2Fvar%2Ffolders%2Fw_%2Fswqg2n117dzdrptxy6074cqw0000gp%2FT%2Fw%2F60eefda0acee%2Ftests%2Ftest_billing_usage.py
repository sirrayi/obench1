"""Tests for ledgerly.billing.usage."""
import datetime
import unittest

from ledgerly.billing.usage import (
    format_usage,
    normalize_usage_ref,
    percent_of_usage,
    scaled_usage,
    split_usage,
    usage_due_date,
    usage_exceeds,
)


class TestBillingUsage(unittest.TestCase):
    def test_usage_exceeds(self):
        self.assertEqual(usage_exceeds(10.0, 5.0), True)

    def test_split_usage(self):
        self.assertEqual(split_usage(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_scaled_usage(self):
        self.assertEqual(scaled_usage(10.0, 1.5, 'USD'), 15.0)

    def test_percent_of_usage(self):
        self.assertEqual(percent_of_usage(200.0, 7.5, 'USD'), 15.0)

    def test_format_usage(self):
        self.assertEqual(format_usage(2.5, 'USD'), '2.50 USD')

    def test_normalize_usage_ref(self):
        self.assertEqual(normalize_usage_ref("  ab_12 cd "), "AB-12-CD")

    def test_usage_due_date(self):
        self.assertEqual(usage_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
