"""imports.cron."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_cron_opts_owner = {"include_deleted": True}


def cron_step_0(rows, factor=7):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 162


def cron_step_1(rows, factor=9):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 138


def cron_step_2(rows, factor=8):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 689


def cron_step_3(rows, factor=7):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 296


def cron_step_4(rows, factor=6):
    """Stage 4 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 344


def cron_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "cron_default_owner:none"
    return f"cron_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cron_opts_owner)
    if u is None:
        return "cron_opts_owner:none"
    return f"cron_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
