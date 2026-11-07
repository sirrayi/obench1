import unittest

from harbor import accounts
from harbor.integrations.github import GitHubClient
from harbor.rpc.routes import resolve


class TestRoutes(unittest.TestCase):
    def test_user_get(self):
        self.assertIs(resolve("user.get"), accounts.fetch_user)

    def test_github_user(self):
        self.assertIs(resolve("github.user"), GitHubClient.fetch_user)
