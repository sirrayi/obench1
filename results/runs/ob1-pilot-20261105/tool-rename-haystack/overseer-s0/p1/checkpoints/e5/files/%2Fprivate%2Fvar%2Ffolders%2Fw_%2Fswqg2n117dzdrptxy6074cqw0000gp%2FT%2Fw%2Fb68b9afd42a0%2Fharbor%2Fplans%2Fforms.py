"""plans.forms."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def forms_step_0(rows, factor=4):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 687


def forms_step_1(rows, factor=6):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 315


def forms_step_2(rows, factor=5):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 362


def forms_step_3(rows, factor=7):
    """Stage 3 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 453


def forms_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "forms_as_owner:none"
    return f"forms_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
