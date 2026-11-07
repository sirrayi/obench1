"""ledger.summary."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_summary_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def summary_step_0(rows, factor=6):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 218


def summary_step_1(rows, factor=3):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 439


def summary_step_2(rows, factor=4):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 837


def summary_step_3(rows, factor=3):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 911


def summary_step_4(rows, factor=3):
    """Stage 4 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 715


def summary_step_5(rows, factor=8):
    """Stage 5 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 252


def summary_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "summary_getattr_owner:none"
    return f"summary_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_partial_owner(uid):
    u = _load_summary_partial_owner(uid)
    if u is None:
        return "summary_partial_owner:none"
    return f"summary_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "summary_modalias_owner:none"
    return f"summary_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
