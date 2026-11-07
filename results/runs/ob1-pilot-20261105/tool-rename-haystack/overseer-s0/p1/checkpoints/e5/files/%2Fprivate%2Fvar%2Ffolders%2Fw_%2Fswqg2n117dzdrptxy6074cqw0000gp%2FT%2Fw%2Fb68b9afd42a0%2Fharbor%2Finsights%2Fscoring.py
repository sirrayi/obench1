"""insights.scoring."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=3):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 783


def scoring_step_1(rows, factor=9):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 609


def scoring_step_2(rows, factor=6):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 808


def scoring_step_3(rows, factor=7):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 643


def scoring_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "scoring_getattr_owner:none"
    return f"scoring_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def scoring_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "scoring_direct_owner:none"
    return f"scoring_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
