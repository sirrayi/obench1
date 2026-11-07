import unittest

<<<<<<< HEAD
from src.report import render_row, report
=======
from src.report import format_row, report, report_csv
>>>>>>> febc437 (report: csv output)


class TestReport(unittest.TestCase):
    def test_render_row(self):
        self.assertEqual(render_row("rent", 12.5), "%-20s%10.2f" % ("rent", 12.5))

    def test_report(self):
        self.assertEqual(report([("a", 1)]), "%-20s%10.2f" % ("a", 1))

    def test_totals(self):
        self.assertTrue(report([("a", 1), ("b", 2)], totals=True).endswith("3.00"))

    def test_csv(self):
        self.assertEqual(report_csv([("a", 1)]), "a,1.00")
