"""mail.audit_log."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)
_OPTS_audit_log_opts_owner = {"include_deleted": True}


def audit_log_step_0(rows, factor=2):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 641


def audit_log_step_1(rows, factor=6):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 261


def audit_log_step_2(rows, factor=7):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 979


def audit_log_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "audit_log_direct_owner:none"
    return f"audit_log_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def audit_log_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_audit_log_opts_owner)
    if u is None:
        return "audit_log_opts_owner:none"
    return f"audit_log_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def audit_log_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "audit_log_default_owner:none"
    return f"audit_log_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def audit_log_population():
    return fetch_user_count() + 11


def audit_log_timer():
    return telemetry.timer("accounts.fetch_user.latency")


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
