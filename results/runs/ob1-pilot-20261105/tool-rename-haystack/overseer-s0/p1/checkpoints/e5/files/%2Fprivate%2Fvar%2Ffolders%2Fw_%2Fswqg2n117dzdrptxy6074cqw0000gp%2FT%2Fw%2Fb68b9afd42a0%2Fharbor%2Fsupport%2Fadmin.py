"""support.admin."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_load_admin_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def admin_step_0(rows, factor=6):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 423


def admin_step_1(rows, factor=3):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 947


def admin_step_2(rows, factor=4):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 391


def admin_step_3(rows, factor=5):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 101


def admin_step_4(rows, factor=8):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 203


def admin_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "admin_as_owner:none"
    return f"admin_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_partial_owner(uid):
    u = _load_admin_partial_owner(uid)
    if u is None:
        return "admin_partial_owner:none"
    return f"admin_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
