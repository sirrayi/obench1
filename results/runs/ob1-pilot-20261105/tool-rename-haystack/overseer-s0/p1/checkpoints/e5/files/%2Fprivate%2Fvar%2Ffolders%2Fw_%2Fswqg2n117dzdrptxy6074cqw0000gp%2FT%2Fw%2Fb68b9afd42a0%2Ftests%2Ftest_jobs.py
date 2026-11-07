import unittest
from unittest import mock

from harbor.jobs import digest
from harbor.jobs import tasks
from harbor.jobs import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestJobs(unittest.TestCase):
    def test_views_direct_owner_mocked(self):
        with mock.patch("harbor.jobs.views.fetch_user", return_value=MOCK):
            self.assertEqual(views.views_direct_owner(3), "views_direct_owner:mocked:pro:0")

    def test_views_direct_owner(self):
        self.assertEqual(views.views_direct_owner(5), "views_direct_owner:user5:team:0")
        self.assertEqual(views.views_direct_owner(14), "views_direct_owner:user14:team:1")

    def test_views_partial_owner(self):
        self.assertEqual(views.views_partial_owner(5), "views_partial_owner:user5:team:0")
        self.assertEqual(views.views_partial_owner(14), "views_partial_owner:user14:team:1")

    def test_tasks_multi_owner_mocked(self):
        with mock.patch("harbor.jobs.tasks.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_multi_owner(3), "tasks_multi_owner:mocked:pro:0")

    def test_tasks_multi_owner(self):
        self.assertEqual(tasks.tasks_multi_owner(5), "tasks_multi_owner:user5:team:0")
        self.assertEqual(tasks.tasks_multi_owner(14), "tasks_multi_owner:none")

    def test_digest_direct_owner_mocked(self):
        with mock.patch("harbor.jobs.digest.fetch_user", return_value=MOCK):
            self.assertEqual(digest.digest_direct_owner(3), "digest_direct_owner:mocked:pro:0")

    def test_digest_direct_owner(self):
        self.assertEqual(digest.digest_direct_owner(5), "digest_direct_owner:user5:team:0")
        self.assertEqual(digest.digest_direct_owner(14), "digest_direct_owner:user14:team:1")
