"""feeds.schema."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def schema_step_0(rows, factor=8):
    """Stage 0 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 431


def schema_step_1(rows, factor=2):
    """Stage 1 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 514


def schema_step_2(rows, factor=4):
    """Stage 2 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 349


def schema_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "schema_as_owner:none"
    return f"schema_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
