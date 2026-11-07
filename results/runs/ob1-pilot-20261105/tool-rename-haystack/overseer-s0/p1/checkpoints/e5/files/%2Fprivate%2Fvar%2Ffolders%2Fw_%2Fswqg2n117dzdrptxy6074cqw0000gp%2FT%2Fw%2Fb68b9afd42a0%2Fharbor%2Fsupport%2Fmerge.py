"""support.merge."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=2):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 164


def merge_step_1(rows, factor=2):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 588


def merge_step_2(rows, factor=4):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 691


def merge_step_3(rows, factor=6):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 178


def merge_step_4(rows, factor=2):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 943


def merge_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "merge_default_owner:none"
    return f"merge_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_population():
    return fetch_user_count() + 17


def merge_timer():
    return telemetry.timer("accounts.fetch_user.calls")
