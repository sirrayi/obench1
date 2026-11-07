import unittest
from unittest import mock

from harbor.uploads import cache
from harbor.uploads import digest
from harbor.uploads import store

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestUploads(unittest.TestCase):
    def test_digest_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(digest.digest_opts_owner(3), "digest_opts_owner:mocked:pro:0")

    def test_digest_opts_owner(self):
        self.assertEqual(digest.digest_opts_owner(5), "digest_opts_owner:user5:team:0")
        self.assertEqual(digest.digest_opts_owner(14), "digest_opts_owner:user14:team:1")

    def test_store_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(store.store_getattr_owner(3), "store_getattr_owner:mocked:pro:0")

    def test_store_getattr_owner(self):
        self.assertEqual(store.store_getattr_owner(5), "store_getattr_owner:user5:team:0")
        self.assertEqual(store.store_getattr_owner(14), "store_getattr_owner:user14:team:1")

    def test_cache_as_owner_mocked(self):
        with mock.patch("harbor.uploads.cache.get_user", return_value=MOCK):
            self.assertEqual(cache.cache_as_owner(3), "cache_as_owner:mocked:pro:0")

    def test_cache_as_owner(self):
        self.assertEqual(cache.cache_as_owner(5), "cache_as_owner:user5:team:0")
        self.assertEqual(cache.cache_as_owner(14), "cache_as_owner:user14:team:1")

    def test_cache_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(cache.cache_opts_owner(3), "cache_opts_owner:mocked:pro:0")

    def test_cache_opts_owner(self):
        self.assertEqual(cache.cache_opts_owner(5), "cache_opts_owner:user5:team:0")
        self.assertEqual(cache.cache_opts_owner(14), "cache_opts_owner:user14:team:1")
