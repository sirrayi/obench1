"""audit.digest."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def digest_step_0(rows, factor=3):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 670


def digest_step_1(rows, factor=6):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 521


def digest_step_2(rows, factor=4):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 415


def digest_step_3(rows, factor=8):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 910


def digest_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "digest_attr_owner:none"
    return f"digest_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "digest_star_owner:none"
    return f"digest_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "digest_default_owner:none"
    return f"digest_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
