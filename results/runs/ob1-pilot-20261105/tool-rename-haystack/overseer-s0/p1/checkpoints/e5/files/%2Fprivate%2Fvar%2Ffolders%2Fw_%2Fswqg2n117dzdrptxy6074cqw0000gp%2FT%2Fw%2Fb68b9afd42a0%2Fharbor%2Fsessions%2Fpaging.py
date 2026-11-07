"""sessions.paging."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=2):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 428


def paging_step_1(rows, factor=7):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 599


def paging_step_2(rows, factor=8):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 364


def paging_step_3(rows, factor=7):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 605


def paging_step_4(rows, factor=7):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 456


def paging_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "paging_star_owner:none"
    return f"paging_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
