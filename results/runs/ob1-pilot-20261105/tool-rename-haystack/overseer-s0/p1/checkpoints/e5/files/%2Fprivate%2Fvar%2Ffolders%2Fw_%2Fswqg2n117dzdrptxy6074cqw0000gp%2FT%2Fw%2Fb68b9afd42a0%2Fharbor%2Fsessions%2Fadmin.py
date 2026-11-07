"""sessions.admin."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def admin_step_0(rows, factor=6):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 462


def admin_step_1(rows, factor=9):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 473


def admin_step_2(rows, factor=7):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 285


def admin_step_3(rows, factor=8):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 911


def admin_step_4(rows, factor=2):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 210


def admin_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "admin_as_owner:none"
    return f"admin_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_timer():
    return telemetry.timer("accounts.fetch_user.latency")
