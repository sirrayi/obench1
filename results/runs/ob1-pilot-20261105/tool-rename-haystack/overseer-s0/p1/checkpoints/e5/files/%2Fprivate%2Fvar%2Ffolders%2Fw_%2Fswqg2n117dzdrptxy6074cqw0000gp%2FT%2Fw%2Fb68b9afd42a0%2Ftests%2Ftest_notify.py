import unittest
from unittest import mock

from harbor.notify import admin
from harbor.notify import digest
from harbor.notify import events
from harbor.notify import forms

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestNotify(unittest.TestCase):
    def test_digest_as_owner_mocked(self):
        with mock.patch("harbor.notify.digest.get_user", return_value=MOCK):
            self.assertEqual(digest.digest_as_owner(3), "digest_as_owner:mocked:pro:0")

    def test_digest_as_owner(self):
        self.assertEqual(digest.digest_as_owner(5), "digest_as_owner:user5:team:0")
        self.assertEqual(digest.digest_as_owner(14), "digest_as_owner:none")

    def test_events_modalias_owner(self):
        self.assertEqual(events.events_modalias_owner(5), "events_modalias_owner:user5:team:0")
        self.assertEqual(events.events_modalias_owner(14), "events_modalias_owner:none")

    def test_admin_attr_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(admin.admin_attr_owner(3), "admin_attr_owner:mocked:pro:0")

    def test_admin_attr_owner(self):
        self.assertEqual(admin.admin_attr_owner(5), "admin_attr_owner:user5:team:0")
        self.assertEqual(admin.admin_attr_owner(14), "admin_attr_owner:none")

    def test_forms_default_owner(self):
        self.assertEqual(forms.forms_default_owner(5), "forms_default_owner:user5:team:0")
        self.assertEqual(forms.forms_default_owner(14), "forms_default_owner:none")
