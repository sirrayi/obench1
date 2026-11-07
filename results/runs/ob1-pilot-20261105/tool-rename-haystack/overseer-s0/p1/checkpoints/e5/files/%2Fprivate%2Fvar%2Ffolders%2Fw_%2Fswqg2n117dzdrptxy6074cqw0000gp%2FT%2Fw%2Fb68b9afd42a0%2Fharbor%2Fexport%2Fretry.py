"""export.retry."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=3):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 384


def retry_step_1(rows, factor=7):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 992


def retry_step_2(rows, factor=2):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 941


def retry_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "retry_modalias_owner:none"
    return f"retry_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "retry_attr_owner:none"
    return f"retry_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "retry_getattr_owner:none"
    return f"retry_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
