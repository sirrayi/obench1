import unittest
from unittest import mock

from harbor.mail import admin
from harbor.mail import queue
from harbor.mail import signals
from harbor.mail import sync

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestMail(unittest.TestCase):
    def test_sync_getattr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(sync.sync_getattr_owner(3), "sync_getattr_owner:mocked:pro:0")

    def test_sync_getattr_owner(self):
        self.assertEqual(sync.sync_getattr_owner(5), "sync_getattr_owner:user5:team:0")
        self.assertEqual(sync.sync_getattr_owner(14), "sync_getattr_owner:none")

    def test_admin_direct_owner_mocked(self):
        with mock.patch("harbor.mail.admin.fetch_user", return_value=MOCK):
            self.assertEqual(admin.admin_direct_owner(3), "admin_direct_owner:mocked:pro:0")

    def test_admin_direct_owner(self):
        self.assertEqual(admin.admin_direct_owner(5), "admin_direct_owner:user5:team:0")
        self.assertEqual(admin.admin_direct_owner(14), "admin_direct_owner:user14:team:1")

    def test_queue_modalias_owner(self):
        self.assertEqual(queue.queue_modalias_owner(5), "queue_modalias_owner:user5:team:0")
        self.assertEqual(queue.queue_modalias_owner(14), "queue_modalias_owner:user14:team:1")

    def test_signals_star_owner(self):
        self.assertEqual(signals.signals_star_owner(5), "signals_star_owner:user5:team:0")
        self.assertEqual(signals.signals_star_owner(14), "signals_star_owner:none")
