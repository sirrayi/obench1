"""quotas.merge."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=2):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 815


def merge_step_1(rows, factor=9):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 379


def merge_step_2(rows, factor=8):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 185


def merge_step_3(rows, factor=9):
    """Stage 3 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 811


def merge_step_4(rows, factor=5):
    """Stage 4 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 773


def merge_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "merge_star_owner:none"
    return f"merge_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
