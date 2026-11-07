"""push.sync."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_sync_opts_owner = {"include_deleted": True}


def sync_step_0(rows, factor=8):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 350


def sync_step_1(rows, factor=2):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 158


def sync_step_2(rows, factor=3):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 950


def sync_step_3(rows, factor=5):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 659


def sync_step_4(rows, factor=3):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 842


def sync_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "sync_star_owner:none"
    return f"sync_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def sync_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_sync_opts_owner)
    if u is None:
        return "sync_opts_owner:none"
    return f"sync_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
