"""audit.paging."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=2):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 472


def paging_step_1(rows, factor=7):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 693


def paging_step_2(rows, factor=2):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 961


def paging_step_3(rows, factor=7):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 220


def paging_step_4(rows, factor=7):
    """Stage 4 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 363


def paging_step_5(rows, factor=5):
    """Stage 5 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 256


def paging_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "paging_default_owner:none"
    return f"paging_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
