"""Tests for ledgerly.invoices.lines."""
import datetime
import unittest

from ledgerly.invoices.lines import (
    accrued_line,
    capped_line,
    line_due_date,
    line_exceeds,
    net_line,
    normalize_line_ref,
    scaled_line,
)


class TestInvoicesLines(unittest.TestCase):
    def test_net_line(self):
        self.assertEqual(net_line(200.0, 10.0, 'USD'), 180.0)

    def test_line_exceeds(self):
        self.assertEqual(line_exceeds(10.0, 5.0), True)

    def test_scaled_line(self):
        self.assertEqual(scaled_line(10.0, 1.5, 'USD'), 15.0)

    def test_capped_line(self):
        self.assertEqual(capped_line(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_accrued_line(self):
        self.assertEqual(accrued_line(36500.0, 10.0, 1, 'USD'), 10.0)

    def test_normalize_line_ref(self):
        self.assertEqual(normalize_line_ref("  ab_12 cd "), "AB-12-CD")

    def test_line_due_date(self):
        self.assertEqual(line_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
