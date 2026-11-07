import unittest

from web import export


class TestExport(unittest.TestCase):
    def test_rows(self):
        out = export.export([{"ts": "2026-10-01T09:00:00", "sensor": "a1", "temp": 20.0}])
        self.assertEqual(out["rows"], ["2026-10-01T09:00:00Z a1 20.0 °C"])
