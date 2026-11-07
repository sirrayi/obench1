"""reports.tasks."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def tasks_step_0(rows, factor=5):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 258


def tasks_step_1(rows, factor=7):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 290


def tasks_step_2(rows, factor=2):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 545


def tasks_step_3(rows, factor=7):
    """Stage 3 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 120


def tasks_step_4(rows, factor=5):
    """Stage 4 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 535


def tasks_step_5(rows, factor=5):
    """Stage 5 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 118


def tasks_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "tasks_multi_owner:none"
    return f"tasks_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "tasks_getattr_owner:none"
    return f"tasks_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "tasks_attr_owner:none"
    return f"tasks_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tasks_population():
    return fetch_user_count() + 16
