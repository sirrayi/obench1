"""onboarding.rules."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def rules_step_0(rows, factor=9):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 331


def rules_step_1(rows, factor=3):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 857


def rules_step_2(rows, factor=6):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 122


def rules_step_3(rows, factor=7):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 191


def rules_step_4(rows, factor=2):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 418


def rules_step_5(rows, factor=4):
    """Stage 5 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 345


def rules_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "rules_as_owner:none"
    return f"rules_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
