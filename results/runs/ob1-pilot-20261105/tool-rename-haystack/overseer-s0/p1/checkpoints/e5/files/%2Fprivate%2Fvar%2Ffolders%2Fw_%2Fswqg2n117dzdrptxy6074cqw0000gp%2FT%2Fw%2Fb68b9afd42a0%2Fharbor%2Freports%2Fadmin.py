"""reports.admin."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_admin_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def admin_step_0(rows, factor=6):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 204


def admin_step_1(rows, factor=9):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 728


def admin_step_2(rows, factor=6):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 599


def admin_step_3(rows, factor=8):
    """Stage 3 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 644


def admin_step_4(rows, factor=8):
    """Stage 4 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 183


def admin_step_5(rows, factor=9):
    """Stage 5 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 623


def admin_partial_owner(uid):
    u = _load_admin_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "admin_partial_owner:none"
    return f"admin_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
