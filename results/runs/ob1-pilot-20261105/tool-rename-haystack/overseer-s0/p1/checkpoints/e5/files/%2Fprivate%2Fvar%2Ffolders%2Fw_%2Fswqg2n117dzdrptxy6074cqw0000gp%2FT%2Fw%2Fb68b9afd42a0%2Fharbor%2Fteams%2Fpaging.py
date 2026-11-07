"""teams.paging."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=9):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 683


def paging_step_1(rows, factor=2):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 384


def paging_step_2(rows, factor=8):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 616


def paging_step_3(rows, factor=9):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 386


def paging_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "paging_star_owner:none"
    return f"paging_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
