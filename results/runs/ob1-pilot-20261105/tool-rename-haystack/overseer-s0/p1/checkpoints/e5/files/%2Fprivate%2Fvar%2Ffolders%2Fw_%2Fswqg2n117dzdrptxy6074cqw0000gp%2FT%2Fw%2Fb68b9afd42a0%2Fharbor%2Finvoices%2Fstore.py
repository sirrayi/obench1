"""invoices.store."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def store_step_0(rows, factor=9):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 326


def store_step_1(rows, factor=4):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 464


def store_step_2(rows, factor=3):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 161


def store_step_3(rows, factor=4):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 249


def store_step_4(rows, factor=9):
    """Stage 4 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 623


def store_step_5(rows, factor=5):
    """Stage 5 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 241


def store_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "store_multi_owner:none"
    return f"store_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def store_population():
    return fetch_user_count() + 3
