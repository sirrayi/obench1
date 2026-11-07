"""analytics.cron."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=6):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 594


def cron_step_1(rows, factor=3):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 871


def cron_step_2(rows, factor=9):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 922


def cron_step_3(rows, factor=6):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 637


def cron_step_4(rows, factor=3):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 923


def cron_step_5(rows, factor=8):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 660


def cron_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_attr_owner:none"
    return f"cron_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_multi_owner:none"
    return f"cron_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_population():
    return fetch_user_count() + 32


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
