import unittest
from unittest import mock

from harbor.webhooks import policy
from harbor.webhooks import rules

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestWebhooks(unittest.TestCase):
    def test_rules_default_owner(self):
        self.assertEqual(rules.rules_default_owner(5), "rules_default_owner:user5:team:0")
        self.assertEqual(rules.rules_default_owner(14), "rules_default_owner:none")

    def test_policy_default_owner(self):
        self.assertEqual(policy.policy_default_owner(5), "policy_default_owner:user5:team:0")
        self.assertEqual(policy.policy_default_owner(14), "policy_default_owner:none")

    def test_policy_star_owner(self):
        self.assertEqual(policy.policy_star_owner(5), "policy_star_owner:user5:team:0")
        self.assertEqual(policy.policy_star_owner(14), "policy_star_owner:none")

    def test_policy_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(policy.policy_getattr_owner(3), "policy_getattr_owner:mocked:pro:0")

    def test_policy_getattr_owner(self):
        self.assertEqual(policy.policy_getattr_owner(5), "policy_getattr_owner:user5:team:0")
        self.assertEqual(policy.policy_getattr_owner(14), "policy_getattr_owner:none")
