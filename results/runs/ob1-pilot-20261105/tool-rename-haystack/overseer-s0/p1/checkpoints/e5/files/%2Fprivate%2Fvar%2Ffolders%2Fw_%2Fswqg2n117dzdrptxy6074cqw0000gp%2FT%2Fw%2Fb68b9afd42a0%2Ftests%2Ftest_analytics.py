import unittest
from unittest import mock

from harbor.analytics import digest
from harbor.analytics import tasks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestAnalytics(unittest.TestCase):
    def test_tasks_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_attr_owner(3), "tasks_attr_owner:mocked:pro:0")

    def test_tasks_attr_owner(self):
        self.assertEqual(tasks.tasks_attr_owner(5), "tasks_attr_owner:user5:team:0")
        self.assertEqual(tasks.tasks_attr_owner(14), "tasks_attr_owner:user14:team:1")

    def test_digest_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(digest.digest_attr_owner(3), "digest_attr_owner:mocked:pro:0")

    def test_digest_attr_owner(self):
        self.assertEqual(digest.digest_attr_owner(5), "digest_attr_owner:user5:team:0")
        self.assertEqual(digest.digest_attr_owner(14), "digest_attr_owner:none")

    def test_digest_modalias_owner(self):
        self.assertEqual(digest.digest_modalias_owner(5), "digest_modalias_owner:user5:team:0")
        self.assertEqual(digest.digest_modalias_owner(14), "digest_modalias_owner:none")

    def test_digest_as_owner_mocked(self):
        with mock.patch("harbor.analytics.digest.get_user", return_value=MOCK):
            self.assertEqual(digest.digest_as_owner(3), "digest_as_owner:mocked:pro:0")

    def test_digest_as_owner(self):
        self.assertEqual(digest.digest_as_owner(5), "digest_as_owner:user5:team:0")
        self.assertEqual(digest.digest_as_owner(14), "digest_as_owner:none")
