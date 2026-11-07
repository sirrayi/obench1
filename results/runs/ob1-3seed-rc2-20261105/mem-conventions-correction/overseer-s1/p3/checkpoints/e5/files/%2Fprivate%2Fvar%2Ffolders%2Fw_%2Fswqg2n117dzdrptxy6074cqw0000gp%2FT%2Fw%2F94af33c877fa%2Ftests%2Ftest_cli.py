import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from tally.cli import main


class TestCli(unittest.TestCase):
    def test_version_flag(self):
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as ctx:
                main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertEqual(out.getvalue(), "tally 1.4.0\n")

    def test_top_command(self):
        old = os.environ.get("TALLY_DB")
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "expenses.csv")
            with open(path, "w") as f:
                f.write("date,amount,category,note\n"
                        "2026-09-01,5.00,food,\n"
                        "2026-10-01,9.00,fun,\n")
            os.environ["TALLY_DB"] = path
            try:
                out = io.StringIO()
                with redirect_stdout(out):
                    main(["top", "1"])
            finally:
                if old is None:
                    del os.environ["TALLY_DB"]
                else:
                    os.environ["TALLY_DB"] = old
        self.assertEqual(out.getvalue(), "2026-10-01 9.00 fun\n")
