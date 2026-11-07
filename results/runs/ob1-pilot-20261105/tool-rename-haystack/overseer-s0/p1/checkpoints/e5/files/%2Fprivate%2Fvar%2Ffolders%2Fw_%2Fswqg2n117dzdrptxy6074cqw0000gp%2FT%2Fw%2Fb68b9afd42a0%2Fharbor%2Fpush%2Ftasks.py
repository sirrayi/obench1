"""push.tasks."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=8):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 790


def tasks_step_1(rows, factor=4):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 871


def tasks_step_2(rows, factor=9):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 644


def tasks_step_3(rows, factor=8):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 300


def tasks_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "tasks_star_owner:none"
    return f"tasks_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "tasks_default_owner:none"
    return f"tasks_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
