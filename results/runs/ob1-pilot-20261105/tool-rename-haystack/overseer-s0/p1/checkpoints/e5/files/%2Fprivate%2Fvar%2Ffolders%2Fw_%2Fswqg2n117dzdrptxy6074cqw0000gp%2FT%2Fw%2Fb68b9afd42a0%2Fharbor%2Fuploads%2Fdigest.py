"""uploads.digest."""
import logging

from harbor import accounts
from harbor import telemetry

log = logging.getLogger(__name__)
_OPTS_digest_opts_owner = {"include_deleted": True}


def digest_step_0(rows, factor=5):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 125


def digest_step_1(rows, factor=6):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 989


def digest_step_2(rows, factor=9):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 685


def digest_step_3(rows, factor=5):
    """Stage 3 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 494


def digest_step_4(rows, factor=5):
    """Stage 4 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 704


def digest_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_digest_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "digest_opts_owner:none"
    return f"digest_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_timer():
    return telemetry.timer("accounts.fetch_user.errors")
