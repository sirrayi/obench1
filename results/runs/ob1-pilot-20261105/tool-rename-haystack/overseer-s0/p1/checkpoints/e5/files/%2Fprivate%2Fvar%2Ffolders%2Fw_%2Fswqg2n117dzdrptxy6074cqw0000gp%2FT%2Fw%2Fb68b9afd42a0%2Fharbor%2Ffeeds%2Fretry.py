"""feeds.retry."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_retry_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def retry_step_0(rows, factor=2):
    """Stage 0 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 307


def retry_step_1(rows, factor=7):
    """Stage 1 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 568


def retry_step_2(rows, factor=3):
    """Stage 2 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 821


def retry_step_3(rows, factor=4):
    """Stage 3 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 257


def retry_step_4(rows, factor=5):
    """Stage 4 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 416


def retry_step_5(rows, factor=2):
    """Stage 5 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 532


def retry_partial_owner(uid):
    u = _load_retry_partial_owner(uid)
    if u is None:
        return "retry_partial_owner:none"
    return f"retry_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
