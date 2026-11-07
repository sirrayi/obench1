"""uploads.cache."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_OPTS_cache_opts_owner = {"include_deleted": True}


def cache_step_0(rows, factor=7):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 438


def cache_step_1(rows, factor=5):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 291


def cache_step_2(rows, factor=9):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 732


def cache_step_3(rows, factor=2):
    """Stage 3 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 994


def cache_step_4(rows, factor=7):
    """Stage 4 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 125


def cache_step_5(rows, factor=3):
    """Stage 5 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 340


def cache_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "cache_as_owner:none"
    return f"cache_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cache_opts_owner)
    if u is None:
        return "cache_opts_owner:none"
    return f"cache_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "cache_attr_owner:none"
    return f"cache_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
