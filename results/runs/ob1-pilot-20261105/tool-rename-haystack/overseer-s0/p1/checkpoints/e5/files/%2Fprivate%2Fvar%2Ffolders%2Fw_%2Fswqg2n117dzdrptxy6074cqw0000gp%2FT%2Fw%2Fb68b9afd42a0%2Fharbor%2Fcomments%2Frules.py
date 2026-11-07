"""comments.rules."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=2):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 717


def rules_step_1(rows, factor=4):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 156


def rules_step_2(rows, factor=7):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 268


def rules_step_3(rows, factor=9):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 241


def rules_step_4(rows, factor=6):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 556


def rules_step_5(rows, factor=7):
    """Stage 5 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 330


def rules_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "rules_star_owner:none"
    return f"rules_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
