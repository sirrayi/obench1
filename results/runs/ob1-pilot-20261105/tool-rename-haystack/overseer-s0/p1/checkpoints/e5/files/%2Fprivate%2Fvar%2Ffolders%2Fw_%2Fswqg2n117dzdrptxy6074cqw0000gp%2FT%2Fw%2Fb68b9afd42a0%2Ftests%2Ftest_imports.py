import unittest
from unittest import mock

from harbor.imports import cache
from harbor.imports import core
from harbor.imports import policy

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestImports(unittest.TestCase):
    def test_core_as_owner_mocked(self):
        with mock.patch("harbor.imports.core.get_user", return_value=MOCK):
            self.assertEqual(core.core_as_owner(3), "core_as_owner:mocked:pro:0")

    def test_core_as_owner(self):
        self.assertEqual(core.core_as_owner(5), "core_as_owner:user5:team:0")
        self.assertEqual(core.core_as_owner(14), "core_as_owner:user14:team:1")

    def test_core_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(core.core_opts_owner(3), "core_opts_owner:mocked:pro:0")

    def test_core_opts_owner(self):
        self.assertEqual(core.core_opts_owner(5), "core_opts_owner:user5:team:0")
        self.assertEqual(core.core_opts_owner(14), "core_opts_owner:user14:team:1")

    def test_policy_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(policy.policy_attr_owner(3), "policy_attr_owner:mocked:pro:0")

    def test_policy_attr_owner(self):
        self.assertEqual(policy.policy_attr_owner(5), "policy_attr_owner:user5:team:0")
        self.assertEqual(policy.policy_attr_owner(14), "policy_attr_owner:user14:team:1")

    def test_cache_partial_owner(self):
        self.assertEqual(cache.cache_partial_owner(5), "cache_partial_owner:user5:team:0")
        self.assertEqual(cache.cache_partial_owner(14), "cache_partial_owner:user14:team:1")
