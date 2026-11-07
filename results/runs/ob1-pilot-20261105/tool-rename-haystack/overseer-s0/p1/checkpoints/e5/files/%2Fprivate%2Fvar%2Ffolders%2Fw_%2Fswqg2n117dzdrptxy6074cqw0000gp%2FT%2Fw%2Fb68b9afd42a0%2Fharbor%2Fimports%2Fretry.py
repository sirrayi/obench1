"""imports.retry."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=2):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 352


def retry_step_1(rows, factor=7):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 511


def retry_step_2(rows, factor=3):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 812


def retry_step_3(rows, factor=5):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 365


def retry_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "retry_multi_owner:none"
    return f"retry_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "retry_getattr_owner:none"
    return f"retry_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_population():
    return fetch_user_count() + 4
