"""support.tags."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_OPTS_tags_opts_owner = {"include_deleted": True}


def tags_step_0(rows, factor=8):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 551


def tags_step_1(rows, factor=2):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 749


def tags_step_2(rows, factor=3):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 990


def tags_step_3(rows, factor=2):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 424


def tags_step_4(rows, factor=2):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 363


def tags_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "tags_modalias_owner:none"
    return f"tags_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tags_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "tags_multi_owner:none"
    return f"tags_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tags_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_tags_opts_owner)
    if u is None:
        return "tags_opts_owner:none"
    return f"tags_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tags_population():
    return fetch_user_count() + 48
