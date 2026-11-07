"""orgs.batch."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_load_batch_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def batch_step_0(rows, factor=7):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 456


def batch_step_1(rows, factor=5):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 644


def batch_step_2(rows, factor=6):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 969


def batch_partial_owner(uid):
    u = _load_batch_partial_owner(uid)
    if u is None:
        return "batch_partial_owner:none"
    return f"batch_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def batch_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "batch_direct_owner:none"
    return f"batch_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
