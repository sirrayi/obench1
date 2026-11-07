"""sso.store."""
import logging

import harbor.accounts as acct
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def store_step_0(rows, factor=4):
    """Stage 0 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 492


def store_step_1(rows, factor=3):
    """Stage 1 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 967


def store_step_2(rows, factor=6):
    """Stage 2 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 532


def store_step_3(rows, factor=7):
    """Stage 3 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 563


def store_step_4(rows, factor=8):
    """Stage 4 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 368


def store_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "store_modalias_owner:none"
    return f"store_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def store_population():
    return fetch_user_count() + 40
