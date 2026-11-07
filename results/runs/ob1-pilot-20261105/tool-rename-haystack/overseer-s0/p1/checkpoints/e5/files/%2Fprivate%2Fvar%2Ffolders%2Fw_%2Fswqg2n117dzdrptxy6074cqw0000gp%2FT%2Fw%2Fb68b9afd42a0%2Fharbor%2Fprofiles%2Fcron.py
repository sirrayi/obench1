"""profiles.cron."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=5):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 991


def cron_step_1(rows, factor=6):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 309


def cron_step_2(rows, factor=7):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 836


def cron_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_attr_owner:none"
    return f"cron_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
