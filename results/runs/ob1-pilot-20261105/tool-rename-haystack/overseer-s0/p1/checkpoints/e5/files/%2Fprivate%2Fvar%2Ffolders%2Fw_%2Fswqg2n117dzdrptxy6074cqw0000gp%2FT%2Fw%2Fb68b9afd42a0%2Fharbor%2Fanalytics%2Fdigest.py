"""analytics.digest."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def digest_step_0(rows, factor=7):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 229


def digest_step_1(rows, factor=6):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 945


def digest_step_2(rows, factor=8):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 481


def digest_step_3(rows, factor=6):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 410


def digest_step_4(rows, factor=9):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 192


def digest_step_5(rows, factor=6):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 358


def digest_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "digest_attr_owner:none"
    return f"digest_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "digest_modalias_owner:none"
    return f"digest_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "digest_as_owner:none"
    return f"digest_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
