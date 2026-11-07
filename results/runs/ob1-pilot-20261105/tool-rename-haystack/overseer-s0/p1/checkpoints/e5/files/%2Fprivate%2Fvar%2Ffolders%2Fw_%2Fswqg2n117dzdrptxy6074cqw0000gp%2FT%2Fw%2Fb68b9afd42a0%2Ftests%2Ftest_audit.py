import unittest
from unittest import mock

from harbor.audit import digest
from harbor.audit import rules

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestAudit(unittest.TestCase):
    def test_rules_modalias_owner(self):
        self.assertEqual(rules.rules_modalias_owner(5), "rules_modalias_owner:user5:team:0")
        self.assertEqual(rules.rules_modalias_owner(14), "rules_modalias_owner:user14:team:1")

    def test_digest_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(digest.digest_attr_owner(3), "digest_attr_owner:mocked:pro:0")

    def test_digest_attr_owner(self):
        self.assertEqual(digest.digest_attr_owner(5), "digest_attr_owner:user5:team:0")
        self.assertEqual(digest.digest_attr_owner(14), "digest_attr_owner:none")

    def test_digest_star_owner(self):
        self.assertEqual(digest.digest_star_owner(5), "digest_star_owner:user5:team:0")
        self.assertEqual(digest.digest_star_owner(14), "digest_star_owner:user14:team:1")

    def test_digest_default_owner(self):
        self.assertEqual(digest.digest_default_owner(5), "digest_default_owner:user5:team:0")
        self.assertEqual(digest.digest_default_owner(14), "digest_default_owner:none")
