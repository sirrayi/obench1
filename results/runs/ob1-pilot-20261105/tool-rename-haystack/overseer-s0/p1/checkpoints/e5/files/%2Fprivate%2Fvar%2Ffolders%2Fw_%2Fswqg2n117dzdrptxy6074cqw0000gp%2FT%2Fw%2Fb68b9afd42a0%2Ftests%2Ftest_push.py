import unittest
from unittest import mock

from harbor.push import sync
from harbor.push import tasks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestPush(unittest.TestCase):
    def test_tasks_star_owner(self):
        self.assertEqual(tasks.tasks_star_owner(5), "tasks_star_owner:user5:team:0")
        self.assertEqual(tasks.tasks_star_owner(14), "tasks_star_owner:none")

    def test_tasks_default_owner(self):
        self.assertEqual(tasks.tasks_default_owner(5), "tasks_default_owner:user5:team:0")
        self.assertEqual(tasks.tasks_default_owner(14), "tasks_default_owner:user14:team:1")

    def test_sync_star_owner(self):
        self.assertEqual(sync.sync_star_owner(5), "sync_star_owner:user5:team:0")
        self.assertEqual(sync.sync_star_owner(14), "sync_star_owner:user14:team:1")

    def test_sync_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(sync.sync_opts_owner(3), "sync_opts_owner:mocked:pro:0")

    def test_sync_opts_owner(self):
        self.assertEqual(sync.sync_opts_owner(5), "sync_opts_owner:user5:team:0")
        self.assertEqual(sync.sync_opts_owner(14), "sync_opts_owner:user14:team:1")
