import io
import unittest
from contextlib import redirect_stdout

from tally import __version__, cli


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
