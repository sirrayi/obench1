import os
import tempfile
import unittest

import sync


class TestSync(unittest.TestCase):
    def test_copies_new_files(self):
        with tempfile.TemporaryDirectory() as s, tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(s, "a"))
            open(os.path.join(s, "a", "x.txt"), "w").write("x")
            sync.main([s, d])
            self.assertTrue(os.path.exists(os.path.join(d, "a", "x.txt")))
