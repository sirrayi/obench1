"""orgs.stats."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def stats_step_0(rows, factor=5):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 660


def stats_step_1(rows, factor=4):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 828


def stats_step_2(rows, factor=8):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 639


def stats_step_3(rows, factor=6):
    """Stage 3 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 634


def stats_step_4(rows, factor=9):
    """Stage 4 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 262


def stats_step_5(rows, factor=9):
    """Stage 5 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 381


def stats_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "stats_multi_owner:none"
    return f"stats_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def stats_population():
    return fetch_user_count() + 52
