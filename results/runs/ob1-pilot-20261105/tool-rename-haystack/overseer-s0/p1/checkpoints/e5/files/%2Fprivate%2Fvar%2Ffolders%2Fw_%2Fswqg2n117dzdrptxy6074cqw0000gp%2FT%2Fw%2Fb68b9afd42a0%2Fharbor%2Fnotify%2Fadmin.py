"""notify.admin."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def admin_step_0(rows, factor=9):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 379


def admin_step_1(rows, factor=6):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 760


def admin_step_2(rows, factor=7):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 603


def admin_step_3(rows, factor=6):
    """Stage 3 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 533


def admin_step_4(rows, factor=2):
    """Stage 4 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 131


def admin_step_5(rows, factor=6):
    """Stage 5 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 167


def admin_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "admin_attr_owner:none"
    return f"admin_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
