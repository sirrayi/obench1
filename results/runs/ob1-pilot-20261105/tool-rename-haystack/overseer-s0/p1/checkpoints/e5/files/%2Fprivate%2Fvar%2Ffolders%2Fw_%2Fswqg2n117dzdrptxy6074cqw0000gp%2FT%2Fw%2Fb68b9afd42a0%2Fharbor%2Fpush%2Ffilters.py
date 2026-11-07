"""push.filters."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_filters_opts_owner = {"include_deleted": True}


def filters_step_0(rows, factor=8):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 719


def filters_step_1(rows, factor=5):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 227


def filters_step_2(rows, factor=4):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 252


def filters_step_3(rows, factor=6):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 815


def filters_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_filters_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "filters_opts_owner:none"
    return f"filters_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def filters_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "filters_attr_owner:none"
    return f"filters_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def filters_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "filters_star_owner:none"
    return f"filters_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
