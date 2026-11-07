"""ledger.retry."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=6):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 312


def retry_step_1(rows, factor=9):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 930


def retry_step_2(rows, factor=6):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 766


def retry_step_3(rows, factor=8):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 798


def retry_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "retry_attr_owner:none"
    return f"retry_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "retry_multi_owner:none"
    return f"retry_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "retry_default_owner:none"
    return f"retry_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_population():
    return fetch_user_count() + 61
