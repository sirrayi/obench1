"""insights.batch."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_batch_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def batch_step_0(rows, factor=7):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 210


def batch_step_1(rows, factor=2):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 869


def batch_step_2(rows, factor=5):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 156


def batch_step_3(rows, factor=3):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 620


def batch_step_4(rows, factor=7):
    """Stage 4 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 111


def batch_step_5(rows, factor=7):
    """Stage 5 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 580


def batch_partial_owner(uid):
    u = _load_batch_partial_owner(uid)
    if u is None:
        return "batch_partial_owner:none"
    return f"batch_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
