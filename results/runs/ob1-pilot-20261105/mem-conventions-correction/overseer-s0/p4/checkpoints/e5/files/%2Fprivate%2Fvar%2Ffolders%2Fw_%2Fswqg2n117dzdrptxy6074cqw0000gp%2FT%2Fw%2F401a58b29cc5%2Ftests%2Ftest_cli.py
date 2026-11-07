import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from tally import cli


class TestCli(unittest.TestCase):
    def test_version_flag(self):
        out = io.StringIO()
        with redirect_stdout(out), self.assertRaises(SystemExit) as raised:
            cli.main(["--version"])
        self.assertEqual(raised.exception.code, 0)
        self.assertEqual(out.getvalue().strip(), "tally 1.4.0")

    def test_sum_still_parses(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "e.csv")
            with open(db, "w", newline="") as f:
                f.write("date,amount,category,note\n")
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"TALLY_DB": db}), redirect_stdout(out):
                self.assertEqual(cli.main(["sum"]), 0)
        self.assertEqual(out.getvalue().strip(), "0.00")

    def test_sum_month_totals_only_that_month(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "e.csv")
            with open(db, "w", newline="") as f:
                f.write("date,amount,category,note\n")
                f.write("2026-09-01,10,food,tea\n")
                f.write("2026-09-30,5.5,travel,\n")
                f.write("2026-10-01,2.25,food,\n")
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"TALLY_DB": db}), redirect_stdout(out):
                self.assertEqual(cli.main(["sum", "--month", "2026-09"]), 0)
        self.assertEqual(out.getvalue().strip(), "15.50")

    def test_sum_month_and_category(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "e.csv")
            with open(db, "w", newline="") as f:
                f.write("date,amount,category,note\n")
                f.write("2026-09-01,10,food,tea\n")
                f.write("2026-09-02,5.5,travel,\n")
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"TALLY_DB": db}), redirect_stdout(out):
                self.assertEqual(cli.main(["sum", "--month", "2026-09", "--category", "food"]), 0)
        self.assertEqual(out.getvalue().strip(), "10.00")

    def test_sum_rejects_malformed_month(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            cli.main(["sum", "--month", "2026-13"])
        self.assertEqual(raised.exception.code, 2)

    def test_top_prints_largest_first(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "e.csv")
            with open(db, "w", newline="") as f:
                f.write("date,amount,category,note\n")
                f.write("2026-09-02,5.5,travel,\n")
                f.write("2026-09-01,9,food,tea\n")
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"TALLY_DB": db}), redirect_stdout(out):
                self.assertEqual(cli.main(["top", "1"]), 0)
        self.assertEqual(out.getvalue().strip(), "2026-09-01 9.00 food")
