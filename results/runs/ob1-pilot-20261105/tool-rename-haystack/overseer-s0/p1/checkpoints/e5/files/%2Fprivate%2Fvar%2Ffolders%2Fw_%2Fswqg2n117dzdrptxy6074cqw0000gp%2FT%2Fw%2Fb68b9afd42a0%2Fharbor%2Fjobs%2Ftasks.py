"""jobs.tasks."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=5):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 375


def tasks_step_1(rows, factor=2):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 299


def tasks_step_2(rows, factor=4):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 543


def tasks_step_3(rows, factor=9):
    """Stage 3 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 987


def tasks_step_4(rows, factor=8):
    """Stage 4 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 256


def tasks_step_5(rows, factor=4):
    """Stage 5 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 940


def tasks_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "tasks_multi_owner:none"
    return f"tasks_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_population():
    return fetch_user_count() + 79
