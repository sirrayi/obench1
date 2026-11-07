import contextlib
import io
import os
import tempfile
import unittest

from tally import cli


class TestCli(unittest.TestCase):
    def run_with_db(self, db_text, argv):
        """Write db_text to a temporary expenses file and run one command."""
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            with open(p, "w") as f:
                f.write(db_text)
            out = io.StringIO()
            old = os.environ.get("TALLY_DB")
            os.environ["TALLY_DB"] = p
            try:
                with contextlib.redirect_stdout(out):
                    cli.main(argv)
            finally:
                if old is None:
                    del os.environ["TALLY_DB"]
                else:
                    os.environ["TALLY_DB"] = old
            return out.getvalue()

    def test_version(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as ctx:
            cli.main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertEqual(out.getvalue(), "tally 1.4.0\n")

    def test_top_prints_largest_first(self):
        got = self.run_with_db("date,amount,category,note\n"
                               "2026-09-02,7.00,fun,\n"
                               "2026-09-01,7.00,books,\n"
                               "2026-09-03,99.50,rent,\n", ["top", "2"])
        self.assertEqual(got, "2026-09-03 99.50 rent\n2026-09-01 7.00 books\n")

    def test_sum_respects_month(self):
        got = self.run_with_db("date,amount,category,note\n"
                               "2026-09-02,7.00,fun,\n"
                               "2026-09-30,3.25,books,\n"
                               "2026-10-01,100.00,rent,\n", ["sum", "--month", "2026-09"])
        self.assertEqual(got, "10.25\n")
