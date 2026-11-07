import unittest
from unittest import mock

from harbor.teams import api
from harbor.teams import digest
from harbor.teams import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestTeams(unittest.TestCase):
    def test_views_default_owner(self):
        self.assertEqual(views.views_default_owner(5), "views_default_owner:user5:team:0")
        self.assertEqual(views.views_default_owner(14), "views_default_owner:none")

    def test_digest_multi_owner_mocked(self):
        with mock.patch("harbor.teams.digest.fetch_user", return_value=MOCK):
            self.assertEqual(digest.digest_multi_owner(3), "digest_multi_owner:mocked:pro:0")

    def test_digest_multi_owner(self):
        self.assertEqual(digest.digest_multi_owner(5), "digest_multi_owner:user5:team:0")
        self.assertEqual(digest.digest_multi_owner(14), "digest_multi_owner:none")

    def test_api_opts_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(api.api_opts_owner(3), "api_opts_owner:mocked:pro:0")

    def test_api_opts_owner(self):
        self.assertEqual(api.api_opts_owner(5), "api_opts_owner:user5:team:0")
        self.assertEqual(api.api_opts_owner(14), "api_opts_owner:user14:team:1")

    def test_api_star_owner(self):
        self.assertEqual(api.api_star_owner(5), "api_star_owner:user5:team:0")
        self.assertEqual(api.api_star_owner(14), "api_star_owner:user14:team:1")
