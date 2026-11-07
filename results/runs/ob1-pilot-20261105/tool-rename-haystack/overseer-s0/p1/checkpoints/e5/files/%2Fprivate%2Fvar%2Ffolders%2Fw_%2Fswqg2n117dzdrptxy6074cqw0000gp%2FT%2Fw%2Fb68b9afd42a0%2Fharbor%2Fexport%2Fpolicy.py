"""export.policy."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=5):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 131


def policy_step_1(rows, factor=8):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 898


def policy_step_2(rows, factor=3):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 146


def policy_step_3(rows, factor=6):
    """Stage 3 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 476


def policy_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "policy_modalias_owner:none"
    return f"policy_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
