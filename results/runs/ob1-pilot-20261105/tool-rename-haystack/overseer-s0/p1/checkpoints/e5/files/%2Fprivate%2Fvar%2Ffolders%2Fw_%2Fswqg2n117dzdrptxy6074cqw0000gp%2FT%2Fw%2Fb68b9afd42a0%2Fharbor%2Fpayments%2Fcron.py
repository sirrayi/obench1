"""payments.cron."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_load_cron_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def cron_step_0(rows, factor=5):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 589


def cron_step_1(rows, factor=6):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 503


def cron_step_2(rows, factor=7):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 698


def cron_partial_owner(uid):
    u = _load_cron_partial_owner(uid)
    if u is None:
        return "cron_partial_owner:none"
    return f"cron_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "cron_as_owner:none"
    return f"cron_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "cron_getattr_owner:none"
    return f"cron_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
