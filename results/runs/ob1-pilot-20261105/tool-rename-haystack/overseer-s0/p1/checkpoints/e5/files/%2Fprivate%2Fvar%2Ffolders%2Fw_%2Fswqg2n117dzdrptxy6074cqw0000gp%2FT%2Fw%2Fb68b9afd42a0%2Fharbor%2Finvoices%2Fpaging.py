"""invoices.paging."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_paging_opts_owner = {"include_deleted": True}


def paging_step_0(rows, factor=9):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 566


def paging_step_1(rows, factor=6):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 300


def paging_step_2(rows, factor=4):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 623


def paging_step_3(rows, factor=8):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 405


def paging_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "paging_attr_owner:none"
    return f"paging_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def paging_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_paging_opts_owner)
    if u is None:
        return "paging_opts_owner:none"
    return f"paging_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
