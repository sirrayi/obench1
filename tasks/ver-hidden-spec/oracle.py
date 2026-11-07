# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

(WS / "daterange.py").write_text(gen.REFERENCE)
(WS / "tests/test_spec.py").write_text('''import datetime
import unittest

from daterange import parse_range

D = datetime.date


class TestSpec(unittest.TestCase):
    def test_month(self):
        self.assertEqual(parse_range("2024-02"), (D(2024, 2, 1), D(2024, 2, 29)))
        self.assertEqual(parse_range("2026-02"), (D(2026, 2, 1), D(2026, 2, 28)))

    def test_week(self):
        self.assertEqual(parse_range("2026-W44"), (D(2026, 10, 26), D(2026, 11, 1)))

    def test_year(self):
        self.assertEqual(parse_range("2026"), (D(2026, 1, 1), D(2026, 12, 31)))

    def test_open(self):
        self.assertEqual(parse_range("..2026-10-31"), (None, D(2026, 10, 31)))
        self.assertEqual(parse_range("2026-10-01.."), (D(2026, 10, 1), None))

    def test_spaces(self):
        self.assertEqual(parse_range("  2026-10-01 .. 2026-10-02 "), (D(2026, 10, 1), D(2026, 10, 2)))

    def test_errors(self):
        for bad in ("..", "2026-10-31..2026-10-01", "2026-13", "2026-W54", "", "2026-02-30", "soon"):
            with self.assertRaises(ValueError, msg=bad):
                parse_range(bad)
''')
