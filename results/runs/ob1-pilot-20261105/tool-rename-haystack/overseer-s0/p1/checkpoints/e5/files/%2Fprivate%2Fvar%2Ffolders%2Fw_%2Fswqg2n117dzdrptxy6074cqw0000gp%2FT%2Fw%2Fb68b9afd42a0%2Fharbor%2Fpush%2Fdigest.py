"""push.digest."""
import logging

from harbor.accounts import fetch_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def digest_step_0(rows, factor=7):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 989


def digest_step_1(rows, factor=6):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 310


def digest_step_2(rows, factor=4):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 832


def digest_step_3(rows, factor=4):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 886


def digest_step_4(rows, factor=4):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 975


def digest_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "digest_direct_owner:none"
    return f"digest_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_population():
    return fetch_user_count() + 6
