"""jobs.digest."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def digest_step_0(rows, factor=6):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 573


def digest_step_1(rows, factor=7):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 391


def digest_step_2(rows, factor=8):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 574


def digest_step_3(rows, factor=2):
    """Stage 3 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 162


def digest_step_4(rows, factor=9):
    """Stage 4 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 330


def digest_step_5(rows, factor=8):
    """Stage 5 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 714


def digest_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "digest_direct_owner:none"
    return f"digest_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
