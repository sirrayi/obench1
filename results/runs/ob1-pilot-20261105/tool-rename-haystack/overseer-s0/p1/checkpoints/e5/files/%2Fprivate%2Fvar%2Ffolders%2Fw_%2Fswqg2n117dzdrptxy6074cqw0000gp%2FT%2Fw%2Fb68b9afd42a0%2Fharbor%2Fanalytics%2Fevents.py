"""analytics.events."""
import logging

import harbor.accounts as acct
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def events_step_0(rows, factor=4):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 863


def events_step_1(rows, factor=3):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 969


def events_step_2(rows, factor=6):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 982


def events_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "events_modalias_owner:none"
    return f"events_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "events_direct_owner:none"
    return f"events_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
