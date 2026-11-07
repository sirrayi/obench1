"""Tests for ledgerly.reports.summaries."""
import datetime
import unittest

from ledgerly.reports.summaries import (
    capped_summary,
    net_summary,
    normalize_summary_ref,
    scaled_summary,
    summary_due_date,
    summary_exceeds,
    summary_settled,
)


class TestReportsSummaries(unittest.TestCase):
    def test_capped_summary(self):
        self.assertEqual(capped_summary(1000.0, 10.0, 50.0, 'USD'), 50.0)

    def test_net_summary(self):
        self.assertEqual(net_summary(200.0, 10.0, 'USD'), 180.0)

    def test_summary_settled(self):
        self.assertEqual(summary_settled(10.0, 10.0), True)

    def test_summary_exceeds(self):
        self.assertEqual(summary_exceeds(10.0, 5.0), True)

    def test_scaled_summary(self):
        self.assertEqual(scaled_summary(10.0, 1.5, 'USD'), 15.0)

    def test_normalize_summary_ref(self):
        self.assertEqual(normalize_summary_ref("  ab_12 cd "), "AB-12-CD")

    def test_summary_due_date(self):
        self.assertEqual(summary_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
