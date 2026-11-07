"""payments.store."""
import functools
import logging

from harbor import accounts
from harbor import telemetry

log = logging.getLogger(__name__)
_load_store_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def store_step_0(rows, factor=6):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 208


def store_step_1(rows, factor=2):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 166


def store_step_2(rows, factor=2):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 733


def store_partial_owner(uid):
    u = _load_store_partial_owner(uid)
    if u is None:
        return "store_partial_owner:none"
    return f"store_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def store_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "store_getattr_owner:none"
    return f"store_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def store_timer():
    return telemetry.timer("accounts.fetch_user.calls")


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
