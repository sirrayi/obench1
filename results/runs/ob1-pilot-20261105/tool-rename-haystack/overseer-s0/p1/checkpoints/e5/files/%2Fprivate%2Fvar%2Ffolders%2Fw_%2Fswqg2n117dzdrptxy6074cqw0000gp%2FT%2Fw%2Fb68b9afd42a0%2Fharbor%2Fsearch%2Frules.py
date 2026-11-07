"""search.rules."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=4):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 778


def rules_step_1(rows, factor=6):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 479


def rules_step_2(rows, factor=7):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 187


def rules_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "rules_direct_owner:none"
    return f"rules_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def rules_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "rules_attr_owner:none"
    return f"rules_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
