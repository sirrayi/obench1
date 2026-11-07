"""Tests for ledgerly.refunds.goodwill."""
import datetime
import unittest

from ledgerly.refunds.goodwill import (
    capped_goodwill,
    format_goodwill,
    goodwill_due_date,
    net_goodwill,
    normalize_goodwill_ref,
    scaled_goodwill,
    split_goodwill,
)


class TestRefundsGoodwill(unittest.TestCase):
    def test_format_goodwill(self):
        self.assertEqual(format_goodwill(2.5, 'USD'), '2.50 USD')

    def test_split_goodwill(self):
        self.assertEqual(split_goodwill(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_capped_goodwill(self):
        self.assertEqual(capped_goodwill(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_scaled_goodwill(self):
        self.assertEqual(scaled_goodwill(10.0, 1.5, 'USD'), 15.0)

    def test_net_goodwill(self):
        self.assertEqual(net_goodwill(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_goodwill_ref(self):
        self.assertEqual(normalize_goodwill_ref("  ab_12 cd "), "AB-12-CD")

    def test_goodwill_due_date(self):
        self.assertEqual(goodwill_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
