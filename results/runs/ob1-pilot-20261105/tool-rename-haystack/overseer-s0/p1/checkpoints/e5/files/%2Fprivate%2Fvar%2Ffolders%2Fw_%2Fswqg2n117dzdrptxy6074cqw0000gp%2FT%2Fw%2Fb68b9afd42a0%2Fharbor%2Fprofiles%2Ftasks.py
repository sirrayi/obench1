"""profiles.tasks."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=2):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 112


def tasks_step_1(rows, factor=7):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 793


def tasks_step_2(rows, factor=5):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 213


def tasks_step_3(rows, factor=8):
    """Stage 3 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 652


def tasks_step_4(rows, factor=5):
    """Stage 4 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 239


def tasks_step_5(rows, factor=3):
    """Stage 5 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 644


def tasks_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "tasks_direct_owner:none"
    return f"tasks_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "tasks_attr_owner:none"
    return f"tasks_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
