"""payments.rules."""
import logging

import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=9):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 869


def rules_step_1(rows, factor=8):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 412


def rules_step_2(rows, factor=9):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 733


def rules_step_3(rows, factor=5):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 581


def rules_step_4(rows, factor=4):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 566


def rules_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "rules_multi_owner:none"
    return f"rules_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def rules_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "rules_modalias_owner:none"
    return f"rules_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def rules_population():
    return fetch_user_count() + 18
