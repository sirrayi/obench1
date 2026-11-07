"""analytics.paging."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=9):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 759


def paging_step_1(rows, factor=2):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 498


def paging_step_2(rows, factor=7):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 426


def paging_step_3(rows, factor=6):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 750


def paging_step_4(rows, factor=6):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 403


def paging_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "paging_star_owner:none"
    return f"paging_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
