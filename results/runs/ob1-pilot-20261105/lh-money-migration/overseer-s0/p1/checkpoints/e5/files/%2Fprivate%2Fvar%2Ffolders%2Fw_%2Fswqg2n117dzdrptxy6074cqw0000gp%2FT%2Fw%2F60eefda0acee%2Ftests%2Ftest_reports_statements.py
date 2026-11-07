"""Tests for ledgerly.reports.statements."""
import datetime
import unittest

from ledgerly.reports.statements import (
    net_statement,
    normalize_statement_ref,
    split_statement,
    statement_due_date,
    statement_exceeds,
    statement_settled,
    total_statement,
)


class TestReportsStatements(unittest.TestCase):
    def test_total_statement(self):
        self.assertEqual(total_statement([1.25, 2.5, 3.0], 'USD'), 6.75)

    def test_statement_settled(self):
        self.assertEqual(statement_settled(10.0, 10.0), True)

    def test_statement_exceeds(self):
        self.assertEqual(statement_exceeds(10.0, 5.0), True)

    def test_split_statement(self):
        self.assertEqual(split_statement(10.0, 4, 'USD'), [2.5, 2.5, 2.5, 2.5])

    def test_net_statement(self):
        self.assertEqual(net_statement(200.0, 10.0, 'USD'), 180.0)

    def test_normalize_statement_ref(self):
        self.assertEqual(normalize_statement_ref("  ab_12 cd "), "AB-12-CD")

    def test_statement_due_date(self):
        self.assertEqual(statement_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))


if __name__ == "__main__":
    unittest.main()
