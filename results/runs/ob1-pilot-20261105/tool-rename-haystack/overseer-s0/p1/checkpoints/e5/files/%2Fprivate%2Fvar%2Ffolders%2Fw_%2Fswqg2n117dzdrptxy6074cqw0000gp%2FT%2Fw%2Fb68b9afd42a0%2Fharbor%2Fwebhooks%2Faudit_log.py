"""webhooks.audit_log."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def audit_log_step_0(rows, factor=7):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 921


def audit_log_step_1(rows, factor=6):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 300


def audit_log_step_2(rows, factor=9):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 364


def audit_log_step_3(rows, factor=4):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 462


def audit_log_step_4(rows, factor=4):
    """Stage 4 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 108


def audit_log_step_5(rows, factor=5):
    """Stage 5 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 719


def audit_log_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "audit_log_default_owner:none"
    return f"audit_log_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
