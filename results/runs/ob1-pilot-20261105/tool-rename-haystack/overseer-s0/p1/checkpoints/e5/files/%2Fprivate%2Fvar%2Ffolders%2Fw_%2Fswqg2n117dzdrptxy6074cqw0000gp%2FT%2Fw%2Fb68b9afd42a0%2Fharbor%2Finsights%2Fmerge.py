"""insights.merge."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_OPTS_merge_opts_owner = {"include_deleted": True}


def merge_step_0(rows, factor=6):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 221


def merge_step_1(rows, factor=8):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 547


def merge_step_2(rows, factor=9):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 626


def merge_step_3(rows, factor=3):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 788


def merge_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_merge_opts_owner)
    if u is None:
        return "merge_opts_owner:none"
    return f"merge_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "merge_direct_owner:none"
    return f"merge_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "merge_modalias_owner:none"
    return f"merge_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
