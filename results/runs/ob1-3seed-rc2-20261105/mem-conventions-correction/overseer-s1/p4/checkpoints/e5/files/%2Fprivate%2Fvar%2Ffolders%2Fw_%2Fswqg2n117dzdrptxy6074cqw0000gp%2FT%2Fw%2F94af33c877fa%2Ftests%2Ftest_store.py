import os
import tempfile
import unittest
from decimal import Decimal

from tally import store


class TestStore(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            store.append({"date": "2026-09-01", "amount": "3.5", "category": "food", "note": "tea"}, p)
            self.assertEqual(store.load(p)[0]["amount"], Decimal("3.50"))
