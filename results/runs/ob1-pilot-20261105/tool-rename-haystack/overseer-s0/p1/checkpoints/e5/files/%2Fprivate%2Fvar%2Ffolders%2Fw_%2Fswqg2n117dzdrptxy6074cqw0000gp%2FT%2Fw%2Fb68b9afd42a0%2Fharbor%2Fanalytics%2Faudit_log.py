"""analytics.audit_log."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def audit_log_step_0(rows, factor=6):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 341


def audit_log_step_1(rows, factor=2):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 197


def audit_log_step_2(rows, factor=4):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 374


def audit_log_step_3(rows, factor=5):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 340


def audit_log_step_4(rows, factor=9):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 122


def audit_log_step_5(rows, factor=8):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 837


def audit_log_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "audit_log_attr_owner:none"
    return f"audit_log_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
