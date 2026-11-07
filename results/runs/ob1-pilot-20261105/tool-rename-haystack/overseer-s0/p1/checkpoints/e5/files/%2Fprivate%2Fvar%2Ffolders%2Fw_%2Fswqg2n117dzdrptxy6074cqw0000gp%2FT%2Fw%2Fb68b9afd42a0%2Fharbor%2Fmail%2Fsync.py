"""mail.sync."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def sync_step_0(rows, factor=4):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 725


def sync_step_1(rows, factor=9):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 197


def sync_step_2(rows, factor=8):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 904


def sync_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "sync_getattr_owner:none"
    return f"sync_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
