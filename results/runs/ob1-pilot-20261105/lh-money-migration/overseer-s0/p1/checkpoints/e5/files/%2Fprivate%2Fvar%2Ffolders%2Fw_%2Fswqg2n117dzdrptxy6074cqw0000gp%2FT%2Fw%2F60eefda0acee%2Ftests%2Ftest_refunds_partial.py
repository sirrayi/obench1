"""Tests for ledgerly.refunds.partial."""
import datetime
import unittest

from ledgerly.refunds.partial import (
    capped_partial_refund,
    net_partial_refund,
    normalize_partial_refund_ref,
    partial_refund_due_date,
    partial_refund_exceeds,
    percent_of_partial_refund,
    split_partial_refund,
)


class TestRefundsPartial(unittest.TestCase):
    def test_partial_refund_exceeds(self):
        self.assertEqual(partial_refund_exceeds(10.0, 5.0), True)

    def test_capped_partial_refund(self):
        self.assertEqual(capped_partial_refund(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_net_partial_refund(self):
        self.assertEqual(net_partial_refund(200.0, 10.0, 'USD'), 180.0)

    def test_percent_of_partial_refund(self):
        self.assertEqual(percent_of_partial_refund(200.0, 7.5, 'USD'), 15.0)

    def test_split_partial_refund(self):
        self.assertEqual(split_partial_refund(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_normalize_partial_refund_ref(self):
        self.assertEqual(normalize_partial_refund_ref("  ab_12 cd "), "AB-12-CD")

    def test_partial_refund_due_date(self):
        self.assertEqual(partial_refund_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
