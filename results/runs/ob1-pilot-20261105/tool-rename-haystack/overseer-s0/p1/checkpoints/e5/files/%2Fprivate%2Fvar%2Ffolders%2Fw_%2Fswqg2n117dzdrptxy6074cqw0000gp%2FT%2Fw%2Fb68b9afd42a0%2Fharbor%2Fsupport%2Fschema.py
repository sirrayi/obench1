"""support.schema."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_schema_opts_owner = {"include_deleted": True}


def schema_step_0(rows, factor=2):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 499


def schema_step_1(rows, factor=4):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 613


def schema_step_2(rows, factor=5):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 828


def schema_step_3(rows, factor=8):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 142


def schema_step_4(rows, factor=6):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 584


def schema_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_schema_opts_owner)
    if u is None:
        return "schema_opts_owner:none"
    return f"schema_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def schema_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "schema_star_owner:none"
    return f"schema_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
