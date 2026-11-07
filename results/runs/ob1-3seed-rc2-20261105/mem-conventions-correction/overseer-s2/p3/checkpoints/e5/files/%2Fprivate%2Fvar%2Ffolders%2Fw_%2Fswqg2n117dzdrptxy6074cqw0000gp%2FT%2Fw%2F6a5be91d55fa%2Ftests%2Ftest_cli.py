import contextlib
import io
import os
import tempfile
import unittest

from tally import cli


class TestCli(unittest.TestCase):
    def test_version(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as ctx:
            cli.main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertEqual(out.getvalue(), "tally 1.4.0\n")

    def test_top_prints_largest_first(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            with open(p, "w") as f:
                f.write("date,amount,category,note\n"
                        "2026-09-02,7.00,fun,\n"
                        "2026-09-01,7.00,books,\n"
                        "2026-09-03,99.50,rent,\n")
            out = io.StringIO()
            old = os.environ.get("TALLY_DB")
            os.environ["TALLY_DB"] = p
            try:
                with contextlib.redirect_stdout(out):
                    cli.main(["top", "2"])
            finally:
                if old is None:
                    del os.environ["TALLY_DB"]
                else:
                    os.environ["TALLY_DB"] = old
            self.assertEqual(out.getvalue(), "2026-09-03 99.50 rent\n2026-09-01 7.00 books\n")
