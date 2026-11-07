"""payments.tasks."""
import logging

import harbor.accounts as acct
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=6):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 559


def tasks_step_1(rows, factor=8):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 515


def tasks_step_2(rows, factor=3):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 180


def tasks_step_3(rows, factor=4):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 744


def tasks_step_4(rows, factor=9):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 240


def tasks_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "tasks_as_owner:none"
    return f"tasks_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "tasks_modalias_owner:none"
    return f"tasks_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
