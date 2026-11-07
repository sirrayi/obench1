"""reports.rules."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=4):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 591


def rules_step_1(rows, factor=8):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 239


def rules_step_2(rows, factor=7):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 916


def rules_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "rules_as_owner:none"
    return f"rules_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
