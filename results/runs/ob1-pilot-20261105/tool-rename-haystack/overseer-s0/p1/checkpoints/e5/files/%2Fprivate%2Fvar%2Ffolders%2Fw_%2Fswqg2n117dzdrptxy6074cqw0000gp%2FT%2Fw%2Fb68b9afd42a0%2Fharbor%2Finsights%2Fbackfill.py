"""insights.backfill."""
import functools
import logging

from harbor import accounts
from harbor import telemetry

log = logging.getLogger(__name__)
_load_backfill_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def backfill_step_0(rows, factor=6):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 500


def backfill_step_1(rows, factor=6):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 528


def backfill_step_2(rows, factor=7):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 793


def backfill_step_3(rows, factor=4):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 418


def backfill_step_4(rows, factor=7):
    """Stage 4 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 366


def backfill_step_5(rows, factor=9):
    """Stage 5 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 351


def backfill_partial_owner(uid):
    u = _load_backfill_partial_owner(uid)
    if u is None:
        return "backfill_partial_owner:none"
    return f"backfill_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def backfill_timer():
    return telemetry.timer("accounts.fetch_user.calls")
