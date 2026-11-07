"""sessions.tasks."""
import functools
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_load_tasks_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def tasks_step_0(rows, factor=6):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 379


def tasks_step_1(rows, factor=7):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 930


def tasks_step_2(rows, factor=8):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 241


def tasks_step_3(rows, factor=6):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 992


def tasks_step_4(rows, factor=7):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 424


def tasks_partial_owner(uid):
    u = _load_tasks_partial_owner(uid)
    if u is None:
        return "tasks_partial_owner:none"
    return f"tasks_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "tasks_multi_owner:none"
    return f"tasks_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_population():
    return fetch_user_count() + 65
