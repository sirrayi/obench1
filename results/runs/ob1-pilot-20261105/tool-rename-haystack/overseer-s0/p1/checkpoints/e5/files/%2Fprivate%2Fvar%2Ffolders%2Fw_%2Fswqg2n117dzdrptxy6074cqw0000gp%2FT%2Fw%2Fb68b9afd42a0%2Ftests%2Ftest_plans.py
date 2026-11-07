import unittest
from unittest import mock

from harbor.plans import forms
from harbor.plans import models
from harbor.plans import store
from harbor.plans import tasks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestPlans(unittest.TestCase):
    def test_tasks_as_owner_mocked(self):
        with mock.patch("harbor.plans.tasks.get_user", return_value=MOCK):
            self.assertEqual(tasks.tasks_as_owner(3), "tasks_as_owner:mocked:pro:0")

    def test_tasks_as_owner(self):
        self.assertEqual(tasks.tasks_as_owner(5), "tasks_as_owner:user5:team:0")
        self.assertEqual(tasks.tasks_as_owner(14), "tasks_as_owner:user14:team:1")

    def test_store_as_owner_mocked(self):
        with mock.patch("harbor.plans.store.get_user", return_value=MOCK):
            self.assertEqual(store.store_as_owner(3), "store_as_owner:mocked:pro:0")

    def test_store_as_owner(self):
        self.assertEqual(store.store_as_owner(5), "store_as_owner:user5:team:0")
        self.assertEqual(store.store_as_owner(14), "store_as_owner:none")

    def test_forms_as_owner_mocked(self):
        with mock.patch("harbor.plans.forms.get_user", return_value=MOCK):
            self.assertEqual(forms.forms_as_owner(3), "forms_as_owner:mocked:pro:0")

    def test_forms_as_owner(self):
        self.assertEqual(forms.forms_as_owner(5), "forms_as_owner:user5:team:0")
        self.assertEqual(forms.forms_as_owner(14), "forms_as_owner:user14:team:1")

    def test_models_direct_owner_mocked(self):
        with mock.patch("harbor.plans.models.fetch_user", return_value=MOCK):
            self.assertEqual(models.models_direct_owner(3), "models_direct_owner:mocked:pro:0")

    def test_models_direct_owner(self):
        self.assertEqual(models.models_direct_owner(5), "models_direct_owner:user5:team:0")
        self.assertEqual(models.models_direct_owner(14), "models_direct_owner:none")
