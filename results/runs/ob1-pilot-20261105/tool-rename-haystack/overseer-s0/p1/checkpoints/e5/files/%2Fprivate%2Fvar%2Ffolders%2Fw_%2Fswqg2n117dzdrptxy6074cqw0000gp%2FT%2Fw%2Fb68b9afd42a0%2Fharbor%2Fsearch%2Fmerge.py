"""search.merge."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def merge_step_0(rows, factor=8):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 973


def merge_step_1(rows, factor=9):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 539


def merge_step_2(rows, factor=3):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 359


def merge_step_3(rows, factor=9):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 628


def merge_step_4(rows, factor=9):
    """Stage 4 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 233


def merge_step_5(rows, factor=3):
    """Stage 5 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 907


def merge_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "merge_as_owner:none"
    return f"merge_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
