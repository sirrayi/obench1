"""ledger.scoring."""
import logging

from harbor import telemetry
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=9):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 469


def scoring_step_1(rows, factor=4):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 578


def scoring_step_2(rows, factor=2):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 270


def scoring_step_3(rows, factor=7):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 828


def scoring_step_4(rows, factor=2):
    """Stage 4 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 351


def scoring_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "scoring_multi_owner:none"
    return f"scoring_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def scoring_population():
    return fetch_user_count() + 56


def scoring_timer():
    return telemetry.timer("accounts.fetch_user.calls")
