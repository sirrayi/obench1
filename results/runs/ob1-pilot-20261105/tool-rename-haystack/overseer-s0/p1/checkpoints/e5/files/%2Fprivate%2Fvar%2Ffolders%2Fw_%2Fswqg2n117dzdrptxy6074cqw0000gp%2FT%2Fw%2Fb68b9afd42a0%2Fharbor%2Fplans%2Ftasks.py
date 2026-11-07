"""plans.tasks."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=4):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 656


def tasks_step_1(rows, factor=7):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 752


def tasks_step_2(rows, factor=9):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 277


def tasks_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "tasks_as_owner:none"
    return f"tasks_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
