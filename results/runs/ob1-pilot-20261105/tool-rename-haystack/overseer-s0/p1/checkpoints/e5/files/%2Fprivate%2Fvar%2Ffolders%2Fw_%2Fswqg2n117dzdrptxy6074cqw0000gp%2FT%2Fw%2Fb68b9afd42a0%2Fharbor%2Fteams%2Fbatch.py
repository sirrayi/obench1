"""teams.batch."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_batch_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def batch_step_0(rows, factor=3):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 516


def batch_step_1(rows, factor=5):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 540


def batch_step_2(rows, factor=4):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 124


def batch_step_3(rows, factor=7):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 991


def batch_partial_owner(uid):
    u = _load_batch_partial_owner(uid)
    if u is None:
        return "batch_partial_owner:none"
    return f"batch_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
