import os
import tempfile
import unittest
from decimal import Decimal

from meridian import report, text
from meridian.ingest import apac, eu

FEEDS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "feeds")


def write(directory, name, body):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


class AmountFormats(unittest.TestCase):
    def test_v1_groups_thousands_with_dots_or_spaces(self):
        self.assertEqual(text.clean_number("1.234,56"), "1234.56")
        self.assertEqual(text.clean_number("1 234,56"), "1234.56")
        self.assertEqual(text.clean_number("426,66"), "426.66")

    def test_v2_uses_a_plain_decimal_point(self):
        self.assertEqual(text.plain_number("1425.01"), "1425.01")
        self.assertEqual(text.plain_number("1,425.01"), "1425.01")
        self.assertEqual(text.plain_number("47.73"), "47.73")


class EuFeed(unittest.TestCase):
    def test_v2_amounts_are_not_read_as_grouped_thousands(self):
        body = (
            "# region: eu\n# format: v2\ndate;account;amount\n"
            "2026-10-03;AC-3413;1425.01\n"
            "2026-10-08;AC-1205;856.98\n"
        )
        with tempfile.TemporaryDirectory() as d:
            rows = eu.read_feed(write(d, "2026-10.csv", body))
        self.assertEqual([r["amount"] for r in rows], [Decimal("1425.01"), Decimal("856.98")])

    def test_v1_amounts_still_parse(self):
        body = "# region: eu\n# format: v1\ndate;account;amount\n2026-09-27;AC-3239;4.014,05\n"
        with tempfile.TemporaryDirectory() as d:
            rows = eu.read_feed(write(d, "2026-09.csv", body))
        self.assertEqual(
            rows,
            [{"date": "2026-09-27", "account": "AC-3239", "amount": Decimal("4014.05")}],
        )

    def test_unsupported_format_is_rejected(self):
        body = "# format: v9\ndate;account;amount\n2026-10-03;AC-3413;1425.01\n"
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                eu.read_feed(write(d, "2026-10.csv", body))

    def test_missing_format_header_is_rejected(self):
        body = "date;account;amount\n2026-10-03;AC-3413;1425.01\n"
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                eu.read_feed(write(d, "2026-10.csv", body))

    def test_october_total_matches_finance(self):
        # Regression for ISSUE-1: the v2 export read as grouped thousands was 100x.
        self.assertEqual(report.total("eu", "2026-10", FEEDS), Decimal("1774765.57"))


class ApacFeed(unittest.TestCase):
    def test_v2_amounts_are_not_read_as_grouped_thousands(self):
        body = "# format: v2\ndate|account|amount\n2026-10-11|AC-1381|2641.49\n"
        with tempfile.TemporaryDirectory() as d:
            rows = apac.load(write(d, "2026-10.csv", body))
        self.assertEqual(rows[0]["amount"], Decimal("2641.49"))

    def test_v1_amounts_still_parse(self):
        body = "# format: v1\ndate|account|amount\n2026-09-02|AC-9426|1 114,82\n"
        with tempfile.TemporaryDirectory() as d:
            rows = apac.load(write(d, "2026-09.csv", body))
        self.assertEqual(rows[0]["amount"], Decimal("1114.82"))
