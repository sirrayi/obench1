"""notify.forms."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def forms_step_0(rows, factor=5):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 152


def forms_step_1(rows, factor=2):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 281


def forms_step_2(rows, factor=4):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 932


def forms_step_3(rows, factor=2):
    """Stage 3 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 339


def forms_step_4(rows, factor=5):
    """Stage 4 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 503


def forms_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "forms_default_owner:none"
    return f"forms_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
