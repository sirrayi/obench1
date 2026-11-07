import unittest
from unittest import mock

from harbor.quotas import batch
from harbor.quotas import events

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestQuotas(unittest.TestCase):
    def test_events_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_attr_owner(3), "events_attr_owner:mocked:pro:0")

    def test_events_attr_owner(self):
        self.assertEqual(events.events_attr_owner(5), "events_attr_owner:user5:team:0")
        self.assertEqual(events.events_attr_owner(14), "events_attr_owner:none")

    def test_events_direct_owner_mocked(self):
        with mock.patch("harbor.quotas.events.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_direct_owner(3), "events_direct_owner:mocked:pro:0")

    def test_events_direct_owner(self):
        self.assertEqual(events.events_direct_owner(5), "events_direct_owner:user5:team:0")
        self.assertEqual(events.events_direct_owner(14), "events_direct_owner:user14:team:1")

    def test_events_partial_owner(self):
        self.assertEqual(events.events_partial_owner(5), "events_partial_owner:user5:team:0")
        self.assertEqual(events.events_partial_owner(14), "events_partial_owner:user14:team:1")

    def test_batch_as_owner_mocked(self):
        with mock.patch("harbor.quotas.batch.get_user", return_value=MOCK):
            self.assertEqual(batch.batch_as_owner(3), "batch_as_owner:mocked:pro:0")

    def test_batch_as_owner(self):
        self.assertEqual(batch.batch_as_owner(5), "batch_as_owner:user5:team:0")
        self.assertEqual(batch.batch_as_owner(14), "batch_as_owner:user14:team:1")
