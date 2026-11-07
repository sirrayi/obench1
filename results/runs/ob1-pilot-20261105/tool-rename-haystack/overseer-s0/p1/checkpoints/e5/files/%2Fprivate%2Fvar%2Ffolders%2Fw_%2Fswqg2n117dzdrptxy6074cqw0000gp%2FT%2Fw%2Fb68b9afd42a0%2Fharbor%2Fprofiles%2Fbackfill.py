"""profiles.backfill."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=3):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 232


def backfill_step_1(rows, factor=7):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 647


def backfill_step_2(rows, factor=9):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 931


def backfill_step_3(rows, factor=9):
    """Stage 3 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 156


def backfill_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "backfill_star_owner:none"
    return f"backfill_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
