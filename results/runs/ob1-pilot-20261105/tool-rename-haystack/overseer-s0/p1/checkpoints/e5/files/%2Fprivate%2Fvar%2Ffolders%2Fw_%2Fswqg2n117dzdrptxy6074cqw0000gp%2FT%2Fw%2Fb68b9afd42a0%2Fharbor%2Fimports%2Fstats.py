"""imports.stats."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def stats_step_0(rows, factor=2):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 101


def stats_step_1(rows, factor=4):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 747


def stats_step_2(rows, factor=3):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 355


def stats_step_3(rows, factor=2):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 260


def stats_step_4(rows, factor=3):
    """Stage 4 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 145


def stats_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "stats_multi_owner:none"
    return f"stats_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def stats_population():
    return fetch_user_count() + 16
