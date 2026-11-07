"""ledger.core."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_core_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def core_step_0(rows, factor=9):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 843


def core_step_1(rows, factor=6):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 889


def core_step_2(rows, factor=8):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 782


def core_step_3(rows, factor=8):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 609


def core_partial_owner(uid):
    u = _load_core_partial_owner(uid)
    if u is None:
        return "core_partial_owner:none"
    return f"core_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
