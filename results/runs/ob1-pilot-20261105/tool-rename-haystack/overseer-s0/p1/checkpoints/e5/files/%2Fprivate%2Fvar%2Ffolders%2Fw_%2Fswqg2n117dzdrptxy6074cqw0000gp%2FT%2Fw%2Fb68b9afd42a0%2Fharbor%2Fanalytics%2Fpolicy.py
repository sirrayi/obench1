"""analytics.policy."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=7):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 369


def policy_step_1(rows, factor=8):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 576


def policy_step_2(rows, factor=9):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 892


def policy_step_3(rows, factor=2):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 548


def policy_step_4(rows, factor=8):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 468


def policy_step_5(rows, factor=2):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 335


def policy_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "policy_direct_owner:none"
    return f"policy_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
