import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from tally import __version__, cli, store


class TestCli(unittest.TestCase):
    def test_version_flag(self):
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertEqual(out.getvalue(), "tally %s\n" % __version__)

    def test_version_text(self):
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit):
                cli.main(["--version"])
        self.assertEqual(out.getvalue(), "tally 1.4.0\n")

    def test_top(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            store.append({"date": "2026-09-01", "amount": "3.50", "category": "food", "note": ""}, p)
            store.append({"date": "2026-09-02", "amount": "12.00", "category": "travel", "note": "taxi"}, p)
            store.append({"date": "2026-09-03", "amount": "7.25", "category": "books", "note": ""}, p)
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"TALLY_DB": p}):
                with redirect_stdout(out):
                    self.assertEqual(cli.main(["top", "2"]), 0)
        self.assertEqual(out.getvalue(), "2026-09-02 12.00 travel\n2026-09-03 7.25 books\n")
