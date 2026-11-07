import unittest
from unittest import mock

from harbor.onboarding import api
from harbor.onboarding import rules
from harbor.onboarding import store
from harbor.onboarding import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestOnboarding(unittest.TestCase):
    def test_views_direct_owner_mocked(self):
        with mock.patch("harbor.onboarding.views.fetch_user", return_value=MOCK):
            self.assertEqual(views.views_direct_owner(3), "views_direct_owner:mocked:pro:0")

    def test_views_direct_owner(self):
        self.assertEqual(views.views_direct_owner(5), "views_direct_owner:user5:team:0")
        self.assertEqual(views.views_direct_owner(14), "views_direct_owner:none")

    def test_rules_as_owner_mocked(self):
        with mock.patch("harbor.onboarding.rules.get_user", return_value=MOCK):
            self.assertEqual(rules.rules_as_owner(3), "rules_as_owner:mocked:pro:0")

    def test_rules_as_owner(self):
        self.assertEqual(rules.rules_as_owner(5), "rules_as_owner:user5:team:0")
        self.assertEqual(rules.rules_as_owner(14), "rules_as_owner:user14:team:1")

    def test_store_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(store.store_getattr_owner(3), "store_getattr_owner:mocked:pro:0")

    def test_store_getattr_owner(self):
        self.assertEqual(store.store_getattr_owner(5), "store_getattr_owner:user5:team:0")
        self.assertEqual(store.store_getattr_owner(14), "store_getattr_owner:none")

    def test_api_star_owner(self):
        self.assertEqual(api.api_star_owner(5), "api_star_owner:user5:team:0")
        self.assertEqual(api.api_star_owner(14), "api_star_owner:user14:team:1")
