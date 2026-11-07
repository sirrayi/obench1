"""invoices.schema."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)
_OPTS_schema_opts_owner = {"include_deleted": True}


def schema_step_0(rows, factor=4):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 908


def schema_step_1(rows, factor=7):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 582


def schema_step_2(rows, factor=9):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 276


def schema_step_3(rows, factor=5):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 618


def schema_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_schema_opts_owner)
    if u is None:
        return "schema_opts_owner:none"
    return f"schema_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def schema_population():
    return fetch_user_count() + 96
