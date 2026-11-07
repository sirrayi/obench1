import unittest
from unittest import mock

from harbor.profiles import cron
from harbor.profiles import queue
from harbor.profiles import tasks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestProfiles(unittest.TestCase):
    def test_tasks_direct_owner_mocked(self):
        with mock.patch("harbor.profiles.tasks.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_direct_owner(3), "tasks_direct_owner:mocked:pro:0")

    def test_tasks_direct_owner(self):
        self.assertEqual(tasks.tasks_direct_owner(5), "tasks_direct_owner:user5:team:0")
        self.assertEqual(tasks.tasks_direct_owner(14), "tasks_direct_owner:none")

    def test_tasks_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_attr_owner(3), "tasks_attr_owner:mocked:pro:0")

    def test_tasks_attr_owner(self):
        self.assertEqual(tasks.tasks_attr_owner(5), "tasks_attr_owner:user5:team:0")
        self.assertEqual(tasks.tasks_attr_owner(14), "tasks_attr_owner:user14:team:1")

    def test_cron_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(cron.cron_attr_owner(3), "cron_attr_owner:mocked:pro:0")

    def test_cron_attr_owner(self):
        self.assertEqual(cron.cron_attr_owner(5), "cron_attr_owner:user5:team:0")
        self.assertEqual(cron.cron_attr_owner(14), "cron_attr_owner:none")

    def test_queue_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(queue.queue_getattr_owner(3), "queue_getattr_owner:mocked:pro:0")

    def test_queue_getattr_owner(self):
        self.assertEqual(queue.queue_getattr_owner(5), "queue_getattr_owner:user5:team:0")
        self.assertEqual(queue.queue_getattr_owner(14), "queue_getattr_owner:user14:team:1")
