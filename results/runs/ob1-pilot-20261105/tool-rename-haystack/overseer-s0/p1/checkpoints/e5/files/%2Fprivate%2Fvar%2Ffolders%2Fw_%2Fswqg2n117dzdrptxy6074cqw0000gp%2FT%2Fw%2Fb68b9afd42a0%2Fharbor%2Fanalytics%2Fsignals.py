"""analytics.signals."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def signals_step_0(rows, factor=3):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 133


def signals_step_1(rows, factor=9):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 656


def signals_step_2(rows, factor=4):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 556


def signals_step_3(rows, factor=7):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 383


def signals_step_4(rows, factor=7):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 577


def signals_step_5(rows, factor=3):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 563


def signals_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "signals_direct_owner:none"
    return f"signals_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_timer():
    return telemetry.timer("accounts.fetch_user.errors")
