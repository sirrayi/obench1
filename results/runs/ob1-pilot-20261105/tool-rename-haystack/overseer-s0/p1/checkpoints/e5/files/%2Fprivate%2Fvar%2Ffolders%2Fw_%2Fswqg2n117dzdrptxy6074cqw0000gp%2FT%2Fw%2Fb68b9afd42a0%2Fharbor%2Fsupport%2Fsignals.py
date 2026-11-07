"""support.signals."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def signals_step_0(rows, factor=9):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 335


def signals_step_1(rows, factor=5):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 182


def signals_step_2(rows, factor=7):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 734


def signals_step_3(rows, factor=2):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 484


def signals_step_4(rows, factor=4):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 980


def signals_step_5(rows, factor=2):
    """Stage 5 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 865


def signals_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "signals_multi_owner:none"
    return f"signals_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_population():
    return fetch_user_count() + 43
