"""comments.audit_log."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def audit_log_step_0(rows, factor=7):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 964


def audit_log_step_1(rows, factor=3):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 297


def audit_log_step_2(rows, factor=2):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 888


def audit_log_step_3(rows, factor=5):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 100


def audit_log_step_4(rows, factor=9):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 974


def audit_log_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "audit_log_direct_owner:none"
    return f"audit_log_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def audit_log_timer():
    return telemetry.timer("accounts.fetch_user.calls")
