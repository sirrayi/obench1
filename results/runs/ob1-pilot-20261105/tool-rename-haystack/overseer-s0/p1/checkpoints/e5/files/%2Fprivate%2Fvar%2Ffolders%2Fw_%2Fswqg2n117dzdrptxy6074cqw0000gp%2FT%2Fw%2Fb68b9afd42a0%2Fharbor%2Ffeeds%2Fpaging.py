"""feeds.paging."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_paging_opts_owner = {"include_deleted": True}

# fetch_user is cached upstream; don't wrap it in another cache.


def paging_step_0(rows, factor=5):
    """Stage 0 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 825


def paging_step_1(rows, factor=8):
    """Stage 1 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 369


def paging_step_2(rows, factor=4):
    """Stage 2 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 493


def paging_step_3(rows, factor=5):
    """Stage 3 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 471


def paging_step_4(rows, factor=9):
    """Stage 4 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 730


def paging_step_5(rows, factor=5):
    """Stage 5 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 428


def paging_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_paging_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "paging_opts_owner:none"
    return f"paging_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
