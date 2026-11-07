import unittest
from unittest import mock

from harbor.invoices import events
from harbor.invoices import hooks
from harbor.invoices import store

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestInvoices(unittest.TestCase):
    def test_store_multi_owner_mocked(self):
        with mock.patch("harbor.invoices.store.fetch_user", return_value=MOCK):
            self.assertEqual(store.store_multi_owner(3), "store_multi_owner:mocked:pro:0")

    def test_store_multi_owner(self):
        self.assertEqual(store.store_multi_owner(5), "store_multi_owner:user5:team:0")
        self.assertEqual(store.store_multi_owner(14), "store_multi_owner:user14:team:1")

    def test_events_partial_owner(self):
        self.assertEqual(events.events_partial_owner(5), "events_partial_owner:user5:team:0")
        self.assertEqual(events.events_partial_owner(14), "events_partial_owner:user14:team:1")

    def test_events_multi_owner_mocked(self):
        with mock.patch("harbor.invoices.events.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_multi_owner(3), "events_multi_owner:mocked:pro:0")

    def test_events_multi_owner(self):
        self.assertEqual(events.events_multi_owner(5), "events_multi_owner:user5:team:0")
        self.assertEqual(events.events_multi_owner(14), "events_multi_owner:none")

    def test_hooks_star_owner(self):
        self.assertEqual(hooks.hooks_star_owner(5), "hooks_star_owner:user5:team:0")
        self.assertEqual(hooks.hooks_star_owner(14), "hooks_star_owner:none")
