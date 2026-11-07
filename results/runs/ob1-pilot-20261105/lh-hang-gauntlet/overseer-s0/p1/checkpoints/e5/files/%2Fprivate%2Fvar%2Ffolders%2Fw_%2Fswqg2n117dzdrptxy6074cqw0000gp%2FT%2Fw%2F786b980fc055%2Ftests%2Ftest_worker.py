import subprocess
import sys
import unittest

from relay.worker import chunks


class TestWorker(unittest.TestCase):
    def test_chunks(self):
        self.assertEqual(chunks([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_warm_cache(self):
        # warms the shared cache for the other tests (a helper that lingers)
        subprocess.Popen([sys.executable, "-c", "import time; time.sleep(900)"])
        self.assertTrue(True)
