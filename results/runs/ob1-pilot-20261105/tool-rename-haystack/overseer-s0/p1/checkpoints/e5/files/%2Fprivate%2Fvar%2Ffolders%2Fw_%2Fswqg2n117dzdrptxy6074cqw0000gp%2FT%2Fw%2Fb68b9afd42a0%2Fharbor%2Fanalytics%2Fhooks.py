"""analytics.hooks."""
import logging

from harbor import telemetry
import harbor.accounts as acct

log = logging.getLogger(__name__)


def hooks_step_0(rows, factor=3):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 381


def hooks_step_1(rows, factor=4):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 262


def hooks_step_2(rows, factor=8):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 477


def hooks_step_3(rows, factor=2):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 417


def hooks_step_4(rows, factor=4):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 126


def hooks_step_5(rows, factor=2):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 824


def hooks_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "hooks_modalias_owner:none"
    return f"hooks_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def hooks_timer():
    return telemetry.timer("accounts.fetch_user.errors")
