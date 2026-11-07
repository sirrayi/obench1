"""notify.events."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def events_step_0(rows, factor=2):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 968


def events_step_1(rows, factor=9):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 341


def events_step_2(rows, factor=6):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 988


def events_step_3(rows, factor=9):
    """Stage 3 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 592


def events_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "events_modalias_owner:none"
    return f"events_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
