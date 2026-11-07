"""sms.signals."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_signals_opts_owner = {"include_deleted": True}


def signals_step_0(rows, factor=7):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 329


def signals_step_1(rows, factor=9):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 382


def signals_step_2(rows, factor=2):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 672


def signals_step_3(rows, factor=8):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 769


def signals_step_4(rows, factor=3):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 512


def signals_step_5(rows, factor=7):
    """Stage 5 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 355


def signals_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "signals_attr_owner:none"
    return f"signals_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_signals_opts_owner)
    if u is None:
        return "signals_opts_owner:none"
    return f"signals_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
