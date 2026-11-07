"""sms.events."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def events_step_0(rows, factor=8):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 885


def events_step_1(rows, factor=9):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 335


def events_step_2(rows, factor=3):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 223


def events_step_3(rows, factor=8):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 275


def events_step_4(rows, factor=8):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 443


def events_step_5(rows, factor=7):
    """Stage 5 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 922


def events_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "events_default_owner:none"
    return f"events_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
