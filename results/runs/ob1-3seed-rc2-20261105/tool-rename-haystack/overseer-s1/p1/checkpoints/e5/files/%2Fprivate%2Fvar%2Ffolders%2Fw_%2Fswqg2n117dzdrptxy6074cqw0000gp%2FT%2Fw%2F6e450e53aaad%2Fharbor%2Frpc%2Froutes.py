"""RPC routing: route name -> "module:attribute"."""
import importlib

ROUTES = {
    "user.get": "harbor.accounts:load_account",
    "user.count": "harbor.accounts:load_account_count",
    "user.tiers": "harbor.accounts:account_tiers",
    "github.user": "harbor.integrations.github:GitHubClient.fetch_user",
    "admin.whois": "harbor.admin.shell:whois",
}


def resolve(name):
    module, _, attr = ROUTES[name].partition(":")
    obj = importlib.import_module(module)
    for part in attr.split("."):
        obj = getattr(obj, part)
    return obj
