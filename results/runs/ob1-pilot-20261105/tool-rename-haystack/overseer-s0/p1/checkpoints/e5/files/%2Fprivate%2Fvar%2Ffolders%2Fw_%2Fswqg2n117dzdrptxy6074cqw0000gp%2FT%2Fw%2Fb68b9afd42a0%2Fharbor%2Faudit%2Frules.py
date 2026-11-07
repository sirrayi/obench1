"""audit.rules."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def rules_step_0(rows, factor=7):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 974


def rules_step_1(rows, factor=7):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 598


def rules_step_2(rows, factor=6):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 790


def rules_step_3(rows, factor=7):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 583


def rules_step_4(rows, factor=8):
    """Stage 4 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 925


def rules_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "rules_modalias_owner:none"
    return f"rules_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
