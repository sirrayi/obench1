"""push.signals."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_signals_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def signals_step_0(rows, factor=8):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 883


def signals_step_1(rows, factor=6):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 518


def signals_step_2(rows, factor=5):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 277


def signals_step_3(rows, factor=8):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 681


def signals_step_4(rows, factor=2):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 472


def signals_step_5(rows, factor=8):
    """Stage 5 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 735


def signals_partial_owner(uid):
    u = _load_signals_partial_owner(uid)
    if u is None:
        return "signals_partial_owner:none"
    return f"signals_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
