"""teams.stats."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_OPTS_stats_opts_owner = {"include_deleted": True}


def stats_step_0(rows, factor=7):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 194


def stats_step_1(rows, factor=6):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 773


def stats_step_2(rows, factor=2):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 680


def stats_step_3(rows, factor=8):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 110


def stats_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "stats_default_owner:none"
    return f"stats_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def stats_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "stats_multi_owner:none"
    return f"stats_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def stats_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_stats_opts_owner)
    if u is None:
        return "stats_opts_owner:none"
    return f"stats_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def stats_population():
    return fetch_user_count() + 92
