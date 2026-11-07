"""imports.scoring."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def scoring_step_0(rows, factor=4):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 258


def scoring_step_1(rows, factor=8):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 951


def scoring_step_2(rows, factor=6):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 103


def scoring_step_3(rows, factor=2):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 212


def scoring_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "scoring_direct_owner:none"
    return f"scoring_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
