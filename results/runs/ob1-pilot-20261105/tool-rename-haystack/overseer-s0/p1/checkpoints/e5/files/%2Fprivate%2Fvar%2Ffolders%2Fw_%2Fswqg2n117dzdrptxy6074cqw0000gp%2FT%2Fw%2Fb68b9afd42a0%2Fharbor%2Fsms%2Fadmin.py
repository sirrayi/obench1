"""sms.admin."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_load_admin_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def admin_step_0(rows, factor=9):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 292


def admin_step_1(rows, factor=2):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 839


def admin_step_2(rows, factor=3):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 551


def admin_step_3(rows, factor=3):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 263


def admin_step_4(rows, factor=6):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 652


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
