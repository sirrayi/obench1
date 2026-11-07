"""jobs.cron."""
import logging

import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=8):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 288


def cron_step_1(rows, factor=2):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 475


def cron_step_2(rows, factor=9):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 686


def cron_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_multi_owner:none"
    return f"cron_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_modalias_owner:none"
    return f"cron_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_population():
    return fetch_user_count() + 27
