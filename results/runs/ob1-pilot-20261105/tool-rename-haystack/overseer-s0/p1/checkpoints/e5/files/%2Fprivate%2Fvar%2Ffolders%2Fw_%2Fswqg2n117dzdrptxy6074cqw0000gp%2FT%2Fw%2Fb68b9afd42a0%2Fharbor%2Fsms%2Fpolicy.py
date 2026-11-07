"""sms.policy."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=5):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 383


def policy_step_1(rows, factor=9):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 956


def policy_step_2(rows, factor=9):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 915


def policy_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "policy_modalias_owner:none"
    return f"policy_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
