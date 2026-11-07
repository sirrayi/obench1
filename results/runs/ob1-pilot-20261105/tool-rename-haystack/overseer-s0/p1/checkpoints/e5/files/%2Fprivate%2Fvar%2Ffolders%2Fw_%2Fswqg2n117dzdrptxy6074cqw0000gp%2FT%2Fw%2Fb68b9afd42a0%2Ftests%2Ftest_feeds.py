import unittest
from unittest import mock

from harbor.feeds import events
from harbor.feeds import schema

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestFeeds(unittest.TestCase):
    def test_events_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_attr_owner(3), "events_attr_owner:mocked:pro:0")

    def test_events_attr_owner(self):
        self.assertEqual(events.events_attr_owner(5), "events_attr_owner:user5:team:0")
        self.assertEqual(events.events_attr_owner(14), "events_attr_owner:none")

    def test_events_default_owner(self):
        self.assertEqual(events.events_default_owner(5), "events_default_owner:user5:team:0")
        self.assertEqual(events.events_default_owner(14), "events_default_owner:none")

    def test_events_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_getattr_owner(3), "events_getattr_owner:mocked:pro:0")

    def test_events_getattr_owner(self):
        self.assertEqual(events.events_getattr_owner(5), "events_getattr_owner:user5:team:0")
        self.assertEqual(events.events_getattr_owner(14), "events_getattr_owner:none")

    def test_schema_as_owner_mocked(self):
        with mock.patch("harbor.feeds.schema.get_user", return_value=MOCK):
            self.assertEqual(schema.schema_as_owner(3), "schema_as_owner:mocked:pro:0")

    def test_schema_as_owner(self):
        self.assertEqual(schema.schema_as_owner(5), "schema_as_owner:user5:team:0")
        self.assertEqual(schema.schema_as_owner(14), "schema_as_owner:none")
