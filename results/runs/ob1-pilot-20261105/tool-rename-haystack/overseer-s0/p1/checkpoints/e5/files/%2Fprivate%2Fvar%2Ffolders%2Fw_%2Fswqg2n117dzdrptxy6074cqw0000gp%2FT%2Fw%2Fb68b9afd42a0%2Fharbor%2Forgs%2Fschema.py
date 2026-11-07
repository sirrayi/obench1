"""orgs.schema."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def schema_step_0(rows, factor=8):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 496


def schema_step_1(rows, factor=4):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 743


def schema_step_2(rows, factor=8):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 525


def schema_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "schema_attr_owner:none"
    return f"schema_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
