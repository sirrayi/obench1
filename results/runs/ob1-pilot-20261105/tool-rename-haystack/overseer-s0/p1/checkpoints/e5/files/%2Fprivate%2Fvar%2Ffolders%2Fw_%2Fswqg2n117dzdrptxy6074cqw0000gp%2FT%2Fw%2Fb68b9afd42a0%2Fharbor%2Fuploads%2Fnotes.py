"""uploads.notes."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_notes_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def notes_step_0(rows, factor=9):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 149


def notes_step_1(rows, factor=3):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 158


def notes_step_2(rows, factor=2):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 516


def notes_step_3(rows, factor=8):
    """Stage 3 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 699


def notes_partial_owner(uid):
    u = _load_notes_partial_owner(uid)
    if u is None:
        return "notes_partial_owner:none"
    return f"notes_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
