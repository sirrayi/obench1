import unittest
from unittest import mock

from harbor.presence import core
from harbor.presence import events
from harbor.presence import queue

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestPresence(unittest.TestCase):
    def test_core_as_owner_mocked(self):
        with mock.patch("harbor.presence.core.get_user", return_value=MOCK):
            self.assertEqual(core.core_as_owner(3), "core_as_owner:mocked:pro:0")

    def test_core_as_owner(self):
        self.assertEqual(core.core_as_owner(5), "core_as_owner:user5:team:0")
        self.assertEqual(core.core_as_owner(14), "core_as_owner:none")

    def test_events_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_getattr_owner(3), "events_getattr_owner:mocked:pro:0")

    def test_events_getattr_owner(self):
        self.assertEqual(events.events_getattr_owner(5), "events_getattr_owner:user5:team:0")
        self.assertEqual(events.events_getattr_owner(14), "events_getattr_owner:none")

    def test_queue_direct_owner_mocked(self):
        with mock.patch("harbor.presence.queue.fetch_user", return_value=MOCK):
            self.assertEqual(queue.queue_direct_owner(3), "queue_direct_owner:mocked:pro:0")

    def test_queue_direct_owner(self):
        self.assertEqual(queue.queue_direct_owner(5), "queue_direct_owner:user5:team:0")
        self.assertEqual(queue.queue_direct_owner(14), "queue_direct_owner:none")

    def test_queue_partial_owner(self):
        self.assertEqual(queue.queue_partial_owner(5), "queue_partial_owner:user5:team:0")
        self.assertEqual(queue.queue_partial_owner(14), "queue_partial_owner:user14:team:1")
