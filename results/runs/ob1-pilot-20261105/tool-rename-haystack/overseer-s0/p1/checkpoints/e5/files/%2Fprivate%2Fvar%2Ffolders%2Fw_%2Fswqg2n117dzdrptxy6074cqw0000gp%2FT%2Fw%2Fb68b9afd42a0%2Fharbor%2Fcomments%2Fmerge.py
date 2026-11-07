"""comments.merge."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=5):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 335


def merge_step_1(rows, factor=5):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 946


def merge_step_2(rows, factor=4):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 844


def merge_step_3(rows, factor=2):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 701


def merge_step_4(rows, factor=3):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 323


def merge_step_5(rows, factor=5):
    """Stage 5 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 419


def merge_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "merge_modalias_owner:none"
    return f"merge_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
