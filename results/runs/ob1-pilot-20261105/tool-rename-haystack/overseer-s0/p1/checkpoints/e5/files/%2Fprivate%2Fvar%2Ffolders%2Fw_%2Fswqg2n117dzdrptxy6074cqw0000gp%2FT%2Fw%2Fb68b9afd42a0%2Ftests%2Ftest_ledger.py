import unittest
from unittest import mock

from harbor.ledger import admin
from harbor.ledger import core
from harbor.ledger import events
from harbor.ledger import hooks

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestLedger(unittest.TestCase):
    def test_core_partial_owner(self):
        self.assertEqual(core.core_partial_owner(5), "core_partial_owner:user5:team:0")
        self.assertEqual(core.core_partial_owner(14), "core_partial_owner:user14:team:1")

    def test_events_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(events.events_opts_owner(3), "events_opts_owner:mocked:pro:0")

    def test_events_opts_owner(self):
        self.assertEqual(events.events_opts_owner(5), "events_opts_owner:user5:team:0")
        self.assertEqual(events.events_opts_owner(14), "events_opts_owner:user14:team:1")

    def test_hooks_modalias_owner(self):
        self.assertEqual(hooks.hooks_modalias_owner(5), "hooks_modalias_owner:user5:team:0")
        self.assertEqual(hooks.hooks_modalias_owner(14), "hooks_modalias_owner:none")

    def test_admin_star_owner(self):
        self.assertEqual(admin.admin_star_owner(5), "admin_star_owner:user5:team:0")
        self.assertEqual(admin.admin_star_owner(14), "admin_star_owner:none")
