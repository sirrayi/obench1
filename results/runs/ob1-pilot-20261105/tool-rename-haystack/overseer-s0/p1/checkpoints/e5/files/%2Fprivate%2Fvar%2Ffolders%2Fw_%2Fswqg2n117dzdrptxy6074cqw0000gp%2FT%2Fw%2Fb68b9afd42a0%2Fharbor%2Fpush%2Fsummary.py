"""push.summary."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_OPTS_summary_opts_owner = {"include_deleted": True}


def summary_step_0(rows, factor=9):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 253


def summary_step_1(rows, factor=2):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 726


def summary_step_2(rows, factor=9):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 733


def summary_step_3(rows, factor=2):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 131


def summary_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "summary_direct_owner:none"
    return f"summary_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_summary_opts_owner)
    if u is None:
        return "summary_opts_owner:none"
    return f"summary_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_timer():
    return telemetry.timer("accounts.fetch_user.errors")
