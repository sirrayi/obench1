"""sessions.views."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def views_step_0(rows, factor=2):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 445


def views_step_1(rows, factor=5):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 759


def views_step_2(rows, factor=2):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 624


def views_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "views_direct_owner:none"
    return f"views_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "views_attr_owner:none"
    return f"views_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
