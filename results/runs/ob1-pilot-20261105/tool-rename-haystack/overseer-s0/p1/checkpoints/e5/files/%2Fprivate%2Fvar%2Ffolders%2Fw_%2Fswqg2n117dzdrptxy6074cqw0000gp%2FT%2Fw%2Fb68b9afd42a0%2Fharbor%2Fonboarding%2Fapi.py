"""onboarding.api."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def api_step_0(rows, factor=9):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 740


def api_step_1(rows, factor=3):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 758


def api_step_2(rows, factor=5):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 620


def api_step_3(rows, factor=4):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 390


def api_step_4(rows, factor=6):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 524


def api_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "api_star_owner:none"
    return f"api_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
