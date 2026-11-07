"""search.paging."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=5):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 257


def paging_step_1(rows, factor=4):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 528


def paging_step_2(rows, factor=8):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 467


def paging_step_3(rows, factor=2):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 808


def paging_step_4(rows, factor=8):
    """Stage 4 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 763


def paging_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "paging_direct_owner:none"
    return f"paging_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
