import unittest
from unittest import mock

from harbor.payments import rules
from harbor.payments import tasks
from harbor.payments import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestPayments(unittest.TestCase):
    def test_views_default_owner(self):
        self.assertEqual(views.views_default_owner(5), "views_default_owner:user5:team:0")
        self.assertEqual(views.views_default_owner(14), "views_default_owner:none")

    def test_tasks_as_owner_mocked(self):
        with mock.patch("harbor.payments.tasks.get_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_as_owner(3), "tasks_as_owner:mocked:pro:0")

    def test_tasks_as_owner(self):
        self.assertEqual(tasks.tasks_as_owner(5), "tasks_as_owner:user5:team:0")
        self.assertEqual(tasks.tasks_as_owner(14), "tasks_as_owner:user14:team:1")

    def test_tasks_modalias_owner(self):
        self.assertEqual(tasks.tasks_modalias_owner(5), "tasks_modalias_owner:user5:team:0")
        self.assertEqual(tasks.tasks_modalias_owner(14), "tasks_modalias_owner:none")

    def test_rules_multi_owner_mocked(self):
        with mock.patch("harbor.payments.rules.fetch_user", return_value=MOCK):
            self.assertEqual(rules.rules_multi_owner(3), "rules_multi_owner:mocked:pro:0")

    def test_rules_multi_owner(self):
        self.assertEqual(rules.rules_multi_owner(5), "rules_multi_owner:user5:team:0")
        self.assertEqual(rules.rules_multi_owner(14), "rules_multi_owner:none")
