import unittest
from unittest import mock

from harbor.insights import admin
from harbor.insights import policy
from harbor.insights import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestInsights(unittest.TestCase):
    def test_views_as_owner_mocked(self):
        with mock.patch("harbor.insights.views.get_user", return_value=MOCK):
            self.assertEqual(views.views_as_owner(3), "views_as_owner:mocked:pro:0")

    def test_views_as_owner(self):
        self.assertEqual(views.views_as_owner(5), "views_as_owner:user5:team:0")
        self.assertEqual(views.views_as_owner(14), "views_as_owner:none")

    def test_views_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(views.views_attr_owner(3), "views_attr_owner:mocked:pro:0")

    def test_views_attr_owner(self):
        self.assertEqual(views.views_attr_owner(5), "views_attr_owner:user5:team:0")
        self.assertEqual(views.views_attr_owner(14), "views_attr_owner:none")

    def test_policy_multi_owner_mocked(self):
        with mock.patch("harbor.insights.policy.fetch_user", return_value=MOCK):
            self.assertEqual(policy.policy_multi_owner(3), "policy_multi_owner:mocked:pro:0")

    def test_policy_multi_owner(self):
        self.assertEqual(policy.policy_multi_owner(5), "policy_multi_owner:user5:team:0")
        self.assertEqual(policy.policy_multi_owner(14), "policy_multi_owner:none")

    def test_admin_default_owner(self):
        self.assertEqual(admin.admin_default_owner(5), "admin_default_owner:user5:team:0")
        self.assertEqual(admin.admin_default_owner(14), "admin_default_owner:none")
