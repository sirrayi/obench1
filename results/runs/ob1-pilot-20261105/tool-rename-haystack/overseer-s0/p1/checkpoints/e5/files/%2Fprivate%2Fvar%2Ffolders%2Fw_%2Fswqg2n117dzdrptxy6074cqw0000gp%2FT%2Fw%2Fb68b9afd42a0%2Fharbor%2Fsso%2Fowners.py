"""sso.owners."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_OPTS_owners_opts_owner = {"include_deleted": True}


def owners_step_0(rows, factor=4):
    """Stage 0 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 97


def owners_step_1(rows, factor=5):
    """Stage 1 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 786


def owners_step_2(rows, factor=7):
    """Stage 2 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 126


def owners_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_owners_opts_owner)
    if u is None:
        return "owners_opts_owner:none"
    return f"owners_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "owners_multi_owner:none"
    return f"owners_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_population():
    return fetch_user_count() + 15


def owners_timer():
    return telemetry.timer("accounts.fetch_user.calls")
