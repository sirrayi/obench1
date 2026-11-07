"""imports.signals."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def signals_step_0(rows, factor=3):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 227


def signals_step_1(rows, factor=6):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 778


def signals_step_2(rows, factor=8):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 852


def signals_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "signals_multi_owner:none"
    return f"signals_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_population():
    return fetch_user_count() + 74
