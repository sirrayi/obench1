"""orgs.summary."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def summary_step_0(rows, factor=9):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 170


def summary_step_1(rows, factor=2):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 773


def summary_step_2(rows, factor=8):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 942


def summary_step_3(rows, factor=9):
    """Stage 3 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 869


def summary_step_4(rows, factor=6):
    """Stage 4 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 847


def summary_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "summary_modalias_owner:none"
    return f"summary_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "summary_multi_owner:none"
    return f"summary_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "summary_attr_owner:none"
    return f"summary_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_population():
    return fetch_user_count() + 70
