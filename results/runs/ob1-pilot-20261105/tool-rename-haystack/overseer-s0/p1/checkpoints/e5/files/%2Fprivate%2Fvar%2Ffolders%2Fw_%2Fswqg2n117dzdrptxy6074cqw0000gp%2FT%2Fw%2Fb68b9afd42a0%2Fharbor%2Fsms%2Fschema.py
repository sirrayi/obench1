"""sms.schema."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_schema_opts_owner = {"include_deleted": True}


def schema_step_0(rows, factor=2):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 703


def schema_step_1(rows, factor=7):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 280


def schema_step_2(rows, factor=8):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 109


def schema_step_3(rows, factor=9):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 916


def schema_step_4(rows, factor=4):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 752


def schema_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_schema_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "schema_opts_owner:none"
    return f"schema_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def schema_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "schema_star_owner:none"
    return f"schema_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
