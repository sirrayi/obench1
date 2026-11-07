"""comments.cron."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=8):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 126


def cron_step_1(rows, factor=4):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 359


def cron_step_2(rows, factor=9):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 715


def cron_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "cron_attr_owner:none"
    return f"cron_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "cron_getattr_owner:none"
    return f"cron_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
