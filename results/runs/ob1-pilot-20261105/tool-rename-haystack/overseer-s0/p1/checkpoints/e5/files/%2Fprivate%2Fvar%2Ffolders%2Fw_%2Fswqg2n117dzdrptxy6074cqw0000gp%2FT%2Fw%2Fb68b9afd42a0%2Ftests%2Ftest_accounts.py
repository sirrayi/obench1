import unittest

from harbor.accounts import fetch_user_count, fetch_user


class TestAccounts(unittest.TestCase):
    def test_get(self):
        self.assertEqual(fetch_user(5)["name"], "user5")

    def test_deleted_hidden(self):
        self.assertIsNone(fetch_user(14))

    def test_deleted_on_request(self):
        self.assertTrue(fetch_user(14, include_deleted=True)["deleted"])

    def test_bad_id(self):
        with self.assertRaises(ValueError):
            fetch_user(0)

    def test_count(self):
        self.assertEqual(fetch_user_count(), 4242)
