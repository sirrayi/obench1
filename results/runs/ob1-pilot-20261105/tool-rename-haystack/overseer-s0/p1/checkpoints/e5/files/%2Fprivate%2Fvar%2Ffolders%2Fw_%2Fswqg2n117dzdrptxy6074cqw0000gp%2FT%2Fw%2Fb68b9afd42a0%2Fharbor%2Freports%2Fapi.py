"""reports.api."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_api_opts_owner = {"include_deleted": True}


def api_step_0(rows, factor=6):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 143


def api_step_1(rows, factor=5):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 500


def api_step_2(rows, factor=8):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 190


def api_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_api_opts_owner)
    if u is None:
        return "api_opts_owner:none"
    return f"api_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
