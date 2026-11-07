"""presence.audit_log."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def audit_log_step_0(rows, factor=4):
    """Stage 0 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 195


def audit_log_step_1(rows, factor=6):
    """Stage 1 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 207


def audit_log_step_2(rows, factor=7):
    """Stage 2 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 311


def audit_log_step_3(rows, factor=6):
    """Stage 3 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 248


def audit_log_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "audit_log_getattr_owner:none"
    return f"audit_log_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def audit_log_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "audit_log_attr_owner:none"
    return f"audit_log_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
