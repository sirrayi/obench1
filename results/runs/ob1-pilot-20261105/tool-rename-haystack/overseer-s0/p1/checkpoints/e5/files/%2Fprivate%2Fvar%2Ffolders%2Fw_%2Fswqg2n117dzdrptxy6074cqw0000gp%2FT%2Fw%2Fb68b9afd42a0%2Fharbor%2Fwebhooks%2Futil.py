"""webhooks.util."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_load_util_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)

# fetch_user is cached upstream; don't wrap it in another cache.


def util_step_0(rows, factor=8):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 247


def util_step_1(rows, factor=8):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 490


def util_step_2(rows, factor=7):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 836


def util_step_3(rows, factor=9):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 847


def util_step_4(rows, factor=4):
    """Stage 4 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 221


def util_step_5(rows, factor=6):
    """Stage 5 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 262


def util_partial_owner(uid):
    u = _load_util_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "util_partial_owner:none"
    return f"util_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def util_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "util_direct_owner:none"
    return f"util_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
