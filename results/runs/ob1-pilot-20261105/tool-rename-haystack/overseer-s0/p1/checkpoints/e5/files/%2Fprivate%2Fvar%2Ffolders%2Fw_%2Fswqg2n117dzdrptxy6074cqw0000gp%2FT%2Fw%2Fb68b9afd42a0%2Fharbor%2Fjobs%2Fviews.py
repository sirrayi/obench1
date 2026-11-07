"""jobs.views."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_load_views_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def views_step_0(rows, factor=9):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 270


def views_step_1(rows, factor=4):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 735


def views_step_2(rows, factor=8):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 298


def views_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "views_direct_owner:none"
    return f"views_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_partial_owner(uid):
    u = _load_views_partial_owner(uid)
    if u is None:
        return "views_partial_owner:none"
    return f"views_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
