"""orgs.backfill."""
import logging

from harbor.accounts import fetch_user as get_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=9):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 828


def backfill_step_1(rows, factor=5):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 939


def backfill_step_2(rows, factor=6):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 952


def backfill_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "backfill_as_owner:none"
    return f"backfill_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def backfill_population():
    return fetch_user_count() + 81
