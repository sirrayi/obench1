"""uploads.cron."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_cron_opts_owner = {"include_deleted": True}


def cron_step_0(rows, factor=5):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 552


def cron_step_1(rows, factor=4):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 441


def cron_step_2(rows, factor=3):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 537


def cron_step_3(rows, factor=9):
    """Stage 3 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 976


def cron_step_4(rows, factor=9):
    """Stage 4 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 975


def cron_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_attr_owner:none"
    return f"cron_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cron_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_opts_owner:none"
    return f"cron_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cron_star_owner:none"
    return f"cron_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
