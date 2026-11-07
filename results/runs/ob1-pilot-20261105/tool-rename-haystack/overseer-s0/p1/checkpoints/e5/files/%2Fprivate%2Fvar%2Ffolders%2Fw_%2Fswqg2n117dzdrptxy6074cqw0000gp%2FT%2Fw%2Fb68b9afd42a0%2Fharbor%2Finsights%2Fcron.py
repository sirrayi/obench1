"""insights.cron."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=3):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 601


def cron_step_1(rows, factor=9):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 788


def cron_step_2(rows, factor=3):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 116


def cron_step_3(rows, factor=2):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 314


def cron_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "cron_attr_owner:none"
    return f"cron_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "cron_star_owner:none"
    return f"cron_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
