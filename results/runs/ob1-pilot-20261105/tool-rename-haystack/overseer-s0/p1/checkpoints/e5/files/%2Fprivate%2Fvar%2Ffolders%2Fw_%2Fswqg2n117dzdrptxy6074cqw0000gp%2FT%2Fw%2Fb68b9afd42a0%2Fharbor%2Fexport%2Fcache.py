"""export.cache."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def cache_step_0(rows, factor=6):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 709


def cache_step_1(rows, factor=7):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 283


def cache_step_2(rows, factor=4):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 396


def cache_step_3(rows, factor=6):
    """Stage 3 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 571


def cache_step_4(rows, factor=6):
    """Stage 4 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 377


def cache_step_5(rows, factor=3):
    """Stage 5 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 948


def cache_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cache_attr_owner:none"
    return f"cache_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
