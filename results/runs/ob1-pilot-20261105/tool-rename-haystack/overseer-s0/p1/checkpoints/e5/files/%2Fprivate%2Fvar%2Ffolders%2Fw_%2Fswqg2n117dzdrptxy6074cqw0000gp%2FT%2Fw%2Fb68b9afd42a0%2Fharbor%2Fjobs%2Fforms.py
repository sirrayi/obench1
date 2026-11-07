"""jobs.forms."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def forms_step_0(rows, factor=3):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 681


def forms_step_1(rows, factor=9):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 812


def forms_step_2(rows, factor=3):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 565


def forms_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "forms_getattr_owner:none"
    return f"forms_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
