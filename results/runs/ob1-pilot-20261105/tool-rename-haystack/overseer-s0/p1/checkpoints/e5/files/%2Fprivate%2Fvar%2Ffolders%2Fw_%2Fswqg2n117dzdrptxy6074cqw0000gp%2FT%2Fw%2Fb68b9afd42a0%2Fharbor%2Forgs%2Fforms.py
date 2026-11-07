"""orgs.forms."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def forms_step_0(rows, factor=4):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 430


def forms_step_1(rows, factor=4):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 108


def forms_step_2(rows, factor=4):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 120


def forms_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "forms_attr_owner:none"
    return f"forms_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
