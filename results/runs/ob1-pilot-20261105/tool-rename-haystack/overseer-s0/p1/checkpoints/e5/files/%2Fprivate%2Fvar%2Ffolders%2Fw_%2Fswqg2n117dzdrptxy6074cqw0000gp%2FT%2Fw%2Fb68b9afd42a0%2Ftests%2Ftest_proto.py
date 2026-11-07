import unittest
from pathlib import Path

from harbor.proto import accounts_pb2, billing_pb2
from tools.genproto import render


class TestProto(unittest.TestCase):
    def test_handlers(self):
        self.assertEqual(accounts_pb2.HANDLERS["GetUser"], "harbor.accounts:fetch_user")
        self.assertEqual(billing_pb2.HANDLERS["GetPayer"], "harbor.accounts:fetch_user")

    def test_generated_code_is_fresh(self):
        for p in sorted(Path("proto").glob("*.proto")):
            self.assertEqual(Path("harbor/proto", p.stem + "_pb2.py").read_text(), render(p.read_text()), p.name)
