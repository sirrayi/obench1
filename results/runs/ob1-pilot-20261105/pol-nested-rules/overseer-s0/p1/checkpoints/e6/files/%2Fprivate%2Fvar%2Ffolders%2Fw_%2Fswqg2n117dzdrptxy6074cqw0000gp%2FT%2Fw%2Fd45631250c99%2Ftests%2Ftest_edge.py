import json
import unittest

from edge import uploader


class TestUploader(unittest.TestCase):
    def test_upload(self):
        out = uploader.upload([{"ts": "2026-10-01T09:00:00", "sensor": "a1", "temp": 20.0}])
        self.assertEqual(out["sent"], 1)
        self.assertEqual(json.loads(out["payload"])["readings"][0][1], "a1")
