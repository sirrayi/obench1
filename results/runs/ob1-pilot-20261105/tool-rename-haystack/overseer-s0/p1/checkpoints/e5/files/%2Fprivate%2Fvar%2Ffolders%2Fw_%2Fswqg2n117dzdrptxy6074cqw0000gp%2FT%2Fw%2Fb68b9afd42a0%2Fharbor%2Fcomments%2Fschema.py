"""comments.schema."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def schema_step_0(rows, factor=2):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 296


def schema_step_1(rows, factor=5):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 573


def schema_step_2(rows, factor=3):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 930


def schema_step_3(rows, factor=6):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 707


def schema_step_4(rows, factor=8):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 232


def schema_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "schema_direct_owner:none"
    return f"schema_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
