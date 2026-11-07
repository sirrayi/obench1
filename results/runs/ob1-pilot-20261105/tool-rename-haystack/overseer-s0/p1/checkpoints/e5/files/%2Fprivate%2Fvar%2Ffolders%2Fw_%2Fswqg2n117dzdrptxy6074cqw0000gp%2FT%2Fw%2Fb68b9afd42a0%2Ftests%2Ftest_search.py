import unittest
from unittest import mock

from harbor.search import rules
from harbor.search import views

MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}


class TestSearch(unittest.TestCase):
    def test_views_star_owner(self):
        self.assertEqual(views.views_star_owner(5), "views_star_owner:user5:team:0")
        self.assertEqual(views.views_star_owner(14), "views_star_owner:user14:team:1")

    def test_views_modalias_owner(self):
        self.assertEqual(views.views_modalias_owner(5), "views_modalias_owner:user5:team:0")
        self.assertEqual(views.views_modalias_owner(14), "views_modalias_owner:none")

    def test_views_default_owner(self):
        self.assertEqual(views.views_default_owner(5), "views_default_owner:user5:team:0")
        self.assertEqual(views.views_default_owner(14), "views_default_owner:none")

    def test_rules_direct_owner_mocked(self):
        with mock.patch("harbor.search.rules.fetch_user", return_value=MOCK):
            self.assertEqual(rules.rules_direct_owner(3), "rules_direct_owner:mocked:pro:0")

    def test_rules_direct_owner(self):
        self.assertEqual(rules.rules_direct_owner(5), "rules_direct_owner:user5:team:0")
        self.assertEqual(rules.rules_direct_owner(14), "rules_direct_owner:none")
