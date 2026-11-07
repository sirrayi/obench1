"""onboarding.signals."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_signals_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)
_OPTS_signals_opts_owner = {"include_deleted": True}

# fetch_user is cached upstream; don't wrap it in another cache.


def signals_step_0(rows, factor=5):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 744


def signals_step_1(rows, factor=3):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 557


def signals_step_2(rows, factor=3):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 141


def signals_step_3(rows, factor=7):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 880


def signals_step_4(rows, factor=4):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 496


def signals_partial_owner(uid):
    u = _load_signals_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "signals_partial_owner:none"
    return f"signals_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "signals_attr_owner:none"
    return f"signals_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_signals_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "signals_opts_owner:none"
    return f"signals_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
