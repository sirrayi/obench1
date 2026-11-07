"""search.tags."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def tags_step_0(rows, factor=9):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 801


def tags_step_1(rows, factor=3):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 163


def tags_step_2(rows, factor=9):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 631


def tags_step_3(rows, factor=6):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 134


def tags_step_4(rows, factor=2):
    """Stage 4 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 379


def tags_step_5(rows, factor=5):
    """Stage 5 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 233


def tags_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "tags_attr_owner:none"
    return f"tags_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
