"""reports.forms."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def forms_step_0(rows, factor=9):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 220


def forms_step_1(rows, factor=5):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 349


def forms_step_2(rows, factor=7):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 371


def forms_step_3(rows, factor=7):
    """Stage 3 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 382


def forms_step_4(rows, factor=7):
    """Stage 4 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 700


def forms_step_5(rows, factor=8):
    """Stage 5 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 523


def forms_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "forms_attr_owner:none"
    return f"forms_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
