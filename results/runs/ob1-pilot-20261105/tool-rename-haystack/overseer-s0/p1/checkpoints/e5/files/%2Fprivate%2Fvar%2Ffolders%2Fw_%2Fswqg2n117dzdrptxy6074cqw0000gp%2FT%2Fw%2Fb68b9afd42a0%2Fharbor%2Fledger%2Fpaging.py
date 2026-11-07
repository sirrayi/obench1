"""ledger.paging."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=6):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 149


def paging_step_1(rows, factor=4):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 181


def paging_step_2(rows, factor=2):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 787


def paging_step_3(rows, factor=2):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 814


def paging_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "paging_attr_owner:none"
    return f"paging_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
