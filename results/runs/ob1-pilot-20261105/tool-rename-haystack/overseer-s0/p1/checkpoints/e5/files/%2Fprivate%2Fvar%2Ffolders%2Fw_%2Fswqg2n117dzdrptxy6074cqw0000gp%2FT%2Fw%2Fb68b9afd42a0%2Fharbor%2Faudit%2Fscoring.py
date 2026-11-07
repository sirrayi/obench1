"""audit.scoring."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=2):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 869


def scoring_step_1(rows, factor=5):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 374


def scoring_step_2(rows, factor=6):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 169


def scoring_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "scoring_multi_owner:none"
    return f"scoring_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def scoring_population():
    return fetch_user_count() + 22
