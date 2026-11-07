"""audit.cron."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=6):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 511


def cron_step_1(rows, factor=2):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 357


def cron_step_2(rows, factor=5):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 762


def cron_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "cron_direct_owner:none"
    return f"cron_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
