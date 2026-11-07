import unittest
from unittest import mock

from harbor.orgs import batch
from harbor.orgs import cache
from harbor.orgs import events

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestOrgs(unittest.TestCase):
    def test_cache_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(cache.cache_opts_owner(3), "cache_opts_owner:mocked:pro:0")

    def test_cache_opts_owner(self):
        self.assertEqual(cache.cache_opts_owner(5), "cache_opts_owner:user5:team:0")
        self.assertEqual(cache.cache_opts_owner(14), "cache_opts_owner:user14:team:1")

    def test_events_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_getattr_owner(3), "events_getattr_owner:mocked:pro:0")

    def test_events_getattr_owner(self):
        self.assertEqual(events.events_getattr_owner(5), "events_getattr_owner:user5:team:0")
        self.assertEqual(events.events_getattr_owner(14), "events_getattr_owner:none")

    def test_events_direct_owner_mocked(self):
        with mock.patch("harbor.orgs.events.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_direct_owner(3), "events_direct_owner:mocked:pro:0")

    def test_events_direct_owner(self):
        self.assertEqual(events.events_direct_owner(5), "events_direct_owner:user5:team:0")
        self.assertEqual(events.events_direct_owner(14), "events_direct_owner:none")

    def test_batch_partial_owner(self):
        self.assertEqual(batch.batch_partial_owner(5), "batch_partial_owner:user5:team:0")
        self.assertEqual(batch.batch_partial_owner(14), "batch_partial_owner:user14:team:1")
