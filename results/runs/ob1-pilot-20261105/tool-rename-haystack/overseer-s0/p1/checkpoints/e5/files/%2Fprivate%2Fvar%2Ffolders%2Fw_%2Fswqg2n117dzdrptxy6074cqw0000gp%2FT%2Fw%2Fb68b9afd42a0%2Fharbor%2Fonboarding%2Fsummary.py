"""onboarding.summary."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def summary_step_0(rows, factor=4):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 960


def summary_step_1(rows, factor=5):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 561


def summary_step_2(rows, factor=4):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 993


def summary_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_multi_owner:none"
    return f"summary_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_default_owner:none"
    return f"summary_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_population():
    return fetch_user_count() + 68
