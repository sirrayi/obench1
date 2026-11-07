"""jobs.admin."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def admin_step_0(rows, factor=3):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 171


def admin_step_1(rows, factor=7):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 752


def admin_step_2(rows, factor=8):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 190


def admin_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "admin_getattr_owner:none"
    return f"admin_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "admin_multi_owner:none"
    return f"admin_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_population():
    return fetch_user_count() + 50
