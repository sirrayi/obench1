"""mail.admin."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def admin_step_0(rows, factor=4):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 595


def admin_step_1(rows, factor=4):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 484


def admin_step_2(rows, factor=3):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 605


def admin_step_3(rows, factor=8):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 330


def admin_step_4(rows, factor=9):
    """Stage 4 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 575


def admin_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "admin_direct_owner:none"
    return f"admin_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
