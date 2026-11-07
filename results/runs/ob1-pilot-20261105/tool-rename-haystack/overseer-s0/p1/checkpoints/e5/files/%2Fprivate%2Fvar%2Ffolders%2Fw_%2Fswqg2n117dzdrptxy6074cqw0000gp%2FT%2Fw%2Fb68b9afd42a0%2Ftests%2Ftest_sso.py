import unittest
from unittest import mock

from harbor.sso import policy
from harbor.sso import store

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestSso(unittest.TestCase):
    def test_policy_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(policy.policy_attr_owner(3), "policy_attr_owner:mocked:pro:0")

    def test_policy_attr_owner(self):
        self.assertEqual(policy.policy_attr_owner(5), "policy_attr_owner:user5:team:0")
        self.assertEqual(policy.policy_attr_owner(14), "policy_attr_owner:none")

    def test_policy_default_owner(self):
        self.assertEqual(policy.policy_default_owner(5), "policy_default_owner:user5:team:0")
        self.assertEqual(policy.policy_default_owner(14), "policy_default_owner:user14:team:1")

    def test_policy_multi_owner_mocked(self):
        with mock.patch("harbor.sso.policy.fetch_user", return_value=MOCK):
            self.assertEqual(policy.policy_multi_owner(3), "policy_multi_owner:mocked:pro:0")

    def test_policy_multi_owner(self):
        self.assertEqual(policy.policy_multi_owner(5), "policy_multi_owner:user5:team:0")
        self.assertEqual(policy.policy_multi_owner(14), "policy_multi_owner:user14:team:1")

    def test_store_modalias_owner(self):
        self.assertEqual(store.store_modalias_owner(5), "store_modalias_owner:user5:team:0")
        self.assertEqual(store.store_modalias_owner(14), "store_modalias_owner:none")
