"""sso.policy."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def policy_step_0(rows, factor=7):
    """Stage 0 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 968


def policy_step_1(rows, factor=2):
    """Stage 1 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 881


def policy_step_2(rows, factor=3):
    """Stage 2 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 903


def policy_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "policy_attr_owner:none"
    return f"policy_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "policy_default_owner:none"
    return f"policy_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "policy_multi_owner:none"
    return f"policy_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_population():
    return fetch_user_count() + 93
