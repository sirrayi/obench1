"""push.merge."""
import logging

from harbor.accounts import fetch_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=9):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 318


def merge_step_1(rows, factor=2):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 638


def merge_step_2(rows, factor=4):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 649


def merge_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "merge_direct_owner:none"
    return f"merge_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_population():
    return fetch_user_count() + 96
