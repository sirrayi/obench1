"""Tests for ledgerly.interest.penalties."""
import datetime
import unittest

from ledgerly.interest.penalties import (
    capped_penalty,
    format_penalty,
    net_penalty,
    normalize_penalty_ref,
    penalty_due_date,
    penalty_exceeds,
    penalty_settled,
)


class TestInterestPenalties(unittest.TestCase):
    def test_capped_penalty(self):
        self.assertEqual(capped_penalty(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_penalty_settled(self):
        self.assertEqual(penalty_settled(10.0, 10.0), True)

    def test_net_penalty(self):
        self.assertEqual(net_penalty(200.0, 10.0, 'USD'), 180.0)

    def test_format_penalty(self):
        self.assertEqual(format_penalty(2.5, 'USD'), '2.50 USD')

    def test_penalty_exceeds(self):
        self.assertEqual(penalty_exceeds(10.0, 5.0), True)

    def test_normalize_penalty_ref(self):
        self.assertEqual(normalize_penalty_ref("  ab_12 cd "), "AB-12-CD")

    def test_penalty_due_date(self):
        self.assertEqual(penalty_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
