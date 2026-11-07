"""mail.notes."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def notes_step_0(rows, factor=8):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 712


def notes_step_1(rows, factor=9):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 161


def notes_step_2(rows, factor=6):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 239


def notes_step_3(rows, factor=7):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 403


def notes_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "notes_star_owner:none"
    return f"notes_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
