import unittest
from unittest import mock

from harbor.reports import core
from harbor.reports import tasks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestReports(unittest.TestCase):
    def test_core_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(core.core_attr_owner(3), "core_attr_owner:mocked:pro:0")

    def test_core_attr_owner(self):
        self.assertEqual(core.core_attr_owner(5), "core_attr_owner:user5:team:0")
        self.assertEqual(core.core_attr_owner(14), "core_attr_owner:user14:team:1")

    def test_tasks_multi_owner_mocked(self):
        with mock.patch("harbor.reports.tasks.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_multi_owner(3), "tasks_multi_owner:mocked:pro:0")

    def test_tasks_multi_owner(self):
        self.assertEqual(tasks.tasks_multi_owner(5), "tasks_multi_owner:user5:team:0")
        self.assertEqual(tasks.tasks_multi_owner(14), "tasks_multi_owner:none")

    def test_tasks_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_getattr_owner(3), "tasks_getattr_owner:mocked:pro:0")

    def test_tasks_getattr_owner(self):
        self.assertEqual(tasks.tasks_getattr_owner(5), "tasks_getattr_owner:user5:team:0")
        self.assertEqual(tasks.tasks_getattr_owner(14), "tasks_getattr_owner:none")

    def test_tasks_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_attr_owner(3), "tasks_attr_owner:mocked:pro:0")

    def test_tasks_attr_owner(self):
        self.assertEqual(tasks.tasks_attr_owner(5), "tasks_attr_owner:user5:team:0")
        self.assertEqual(tasks.tasks_attr_owner(14), "tasks_attr_owner:user14:team:1")
