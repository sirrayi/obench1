"""reports.core."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def core_step_0(rows, factor=5):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 250


def core_step_1(rows, factor=9):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 471


def core_step_2(rows, factor=9):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 947


def core_step_3(rows, factor=6):
    """Stage 3 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 305


def core_step_4(rows, factor=7):
    """Stage 4 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 612


def core_step_5(rows, factor=3):
    """Stage 5 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 319


def core_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "core_attr_owner:none"
    return f"core_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
