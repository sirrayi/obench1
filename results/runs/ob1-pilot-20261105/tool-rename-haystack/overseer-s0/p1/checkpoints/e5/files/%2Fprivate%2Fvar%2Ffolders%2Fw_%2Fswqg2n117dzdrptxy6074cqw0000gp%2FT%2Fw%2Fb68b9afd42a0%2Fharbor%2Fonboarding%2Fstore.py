"""onboarding.store."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def store_step_0(rows, factor=7):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 375


def store_step_1(rows, factor=5):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 440


def store_step_2(rows, factor=6):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 770


def store_step_3(rows, factor=6):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 794


def store_step_4(rows, factor=9):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 202


def store_step_5(rows, factor=2):
    """Stage 5 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 136


def store_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "store_getattr_owner:none"
    return f"store_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
