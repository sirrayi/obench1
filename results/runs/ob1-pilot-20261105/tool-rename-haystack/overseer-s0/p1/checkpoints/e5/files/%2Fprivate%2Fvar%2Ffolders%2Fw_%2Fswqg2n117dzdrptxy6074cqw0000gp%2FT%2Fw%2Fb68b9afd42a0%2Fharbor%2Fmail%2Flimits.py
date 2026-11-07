"""mail.limits."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def limits_step_0(rows, factor=6):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 676


def limits_step_1(rows, factor=4):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 740


def limits_step_2(rows, factor=3):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 659


def limits_step_3(rows, factor=5):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 332


def limits_step_4(rows, factor=9):
    """Stage 4 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 521


def limits_step_5(rows, factor=4):
    """Stage 5 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 301


def limits_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "limits_default_owner:none"
    return f"limits_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def limits_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "limits_direct_owner:none"
    return f"limits_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
