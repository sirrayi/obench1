"""ledger.hooks."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def hooks_step_0(rows, factor=4):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 946


def hooks_step_1(rows, factor=7):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 730


def hooks_step_2(rows, factor=5):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 560


def hooks_step_3(rows, factor=2):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 820


def hooks_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "hooks_modalias_owner:none"
    return f"hooks_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
