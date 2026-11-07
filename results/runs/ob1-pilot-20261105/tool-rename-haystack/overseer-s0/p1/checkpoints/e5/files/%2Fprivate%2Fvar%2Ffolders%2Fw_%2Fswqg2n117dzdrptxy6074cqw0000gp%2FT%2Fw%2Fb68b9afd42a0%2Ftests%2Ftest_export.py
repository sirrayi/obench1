import unittest
from unittest import mock

from harbor.export import batch
from harbor.export import cache
from harbor.export import policy
from harbor.export import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestExport(unittest.TestCase):
    def test_views_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(views.views_attr_owner(3), "views_attr_owner:mocked:pro:0")

    def test_views_attr_owner(self):
        self.assertEqual(views.views_attr_owner(5), "views_attr_owner:user5:team:0")
        self.assertEqual(views.views_attr_owner(14), "views_attr_owner:none")

    def test_policy_modalias_owner(self):
        self.assertEqual(policy.policy_modalias_owner(5), "policy_modalias_owner:user5:team:0")
        self.assertEqual(policy.policy_modalias_owner(14), "policy_modalias_owner:user14:team:1")

    def test_cache_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(cache.cache_attr_owner(3), "cache_attr_owner:mocked:pro:0")

    def test_cache_attr_owner(self):
        self.assertEqual(cache.cache_attr_owner(5), "cache_attr_owner:user5:team:0")
        self.assertEqual(cache.cache_attr_owner(14), "cache_attr_owner:none")

    def test_batch_default_owner(self):
        self.assertEqual(batch.batch_default_owner(5), "batch_default_owner:user5:team:0")
        self.assertEqual(batch.batch_default_owner(14), "batch_default_owner:none")
