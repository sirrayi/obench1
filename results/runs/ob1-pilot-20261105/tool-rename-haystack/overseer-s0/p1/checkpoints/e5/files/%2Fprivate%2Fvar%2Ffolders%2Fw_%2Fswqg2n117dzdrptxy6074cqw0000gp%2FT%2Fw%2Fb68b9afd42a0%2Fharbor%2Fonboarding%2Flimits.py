"""onboarding.limits."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_limits_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def limits_step_0(rows, factor=6):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 360


def limits_step_1(rows, factor=2):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 467


def limits_step_2(rows, factor=6):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 569


def limits_step_3(rows, factor=5):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 744


def limits_partial_owner(uid):
    u = _load_limits_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "limits_partial_owner:none"
    return f"limits_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
