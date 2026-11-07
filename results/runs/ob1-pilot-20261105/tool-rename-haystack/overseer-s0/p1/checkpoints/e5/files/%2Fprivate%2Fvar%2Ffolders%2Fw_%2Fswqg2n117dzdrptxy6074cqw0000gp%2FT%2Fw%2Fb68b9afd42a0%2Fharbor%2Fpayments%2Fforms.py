"""payments.forms."""
import functools
import logging

from harbor import accounts
from harbor import telemetry

log = logging.getLogger(__name__)
_load_forms_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def forms_step_0(rows, factor=7):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 288


def forms_step_1(rows, factor=3):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 245


def forms_step_2(rows, factor=6):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 332


def forms_step_3(rows, factor=3):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 666


def forms_step_4(rows, factor=2):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 974


def forms_partial_owner(uid):
    u = _load_forms_partial_owner(uid)
    if u is None:
        return "forms_partial_owner:none"
    return f"forms_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def forms_timer():
    return telemetry.timer("accounts.fetch_user.errors")
