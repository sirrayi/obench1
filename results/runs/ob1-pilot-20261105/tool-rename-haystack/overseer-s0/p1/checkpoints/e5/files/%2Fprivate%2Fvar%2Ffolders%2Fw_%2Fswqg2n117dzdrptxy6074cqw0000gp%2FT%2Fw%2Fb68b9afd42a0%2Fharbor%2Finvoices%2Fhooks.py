"""invoices.hooks."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def hooks_step_0(rows, factor=9):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 494


def hooks_step_1(rows, factor=6):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 707


def hooks_step_2(rows, factor=6):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 275


def hooks_step_3(rows, factor=4):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 805


def hooks_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "hooks_star_owner:none"
    return f"hooks_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
