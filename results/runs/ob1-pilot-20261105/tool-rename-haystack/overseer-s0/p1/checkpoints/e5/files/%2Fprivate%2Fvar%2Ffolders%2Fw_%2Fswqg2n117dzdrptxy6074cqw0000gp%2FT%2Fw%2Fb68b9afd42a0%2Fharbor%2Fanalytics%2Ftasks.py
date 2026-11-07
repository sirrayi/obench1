"""analytics.tasks."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=3):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 754


def tasks_step_1(rows, factor=3):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 464


def tasks_step_2(rows, factor=9):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 519


def tasks_step_3(rows, factor=7):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 791


def tasks_step_4(rows, factor=2):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 812


def tasks_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "tasks_attr_owner:none"
    return f"tasks_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
