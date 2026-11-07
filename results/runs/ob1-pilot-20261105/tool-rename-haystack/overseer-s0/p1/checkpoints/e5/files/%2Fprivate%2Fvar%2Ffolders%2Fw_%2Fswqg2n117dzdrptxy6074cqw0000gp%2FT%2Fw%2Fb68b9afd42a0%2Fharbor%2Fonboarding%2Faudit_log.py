"""onboarding.audit_log."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def audit_log_step_0(rows, factor=7):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 597


def audit_log_step_1(rows, factor=9):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 740


def audit_log_step_2(rows, factor=5):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 389


def audit_log_step_3(rows, factor=3):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 913


def audit_log_step_4(rows, factor=3):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 821


def audit_log_step_5(rows, factor=3):
    """Stage 5 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 292


def audit_log_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "audit_log_direct_owner:none"
    return f"audit_log_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
