"""search.stats."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def stats_step_0(rows, factor=4):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 495


def stats_step_1(rows, factor=6):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 292


def stats_step_2(rows, factor=5):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 577


def stats_step_3(rows, factor=9):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 454


def stats_step_4(rows, factor=6):
    """Stage 4 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 594


def stats_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "stats_modalias_owner:none"
    return f"stats_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
