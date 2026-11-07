"""billing.forms."""
import logging

import harbor.accounts as acct
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def forms_step_0(rows, factor=4):
    """Stage 0 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 390


def forms_step_1(rows, factor=5):
    """Stage 1 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 578


def forms_step_2(rows, factor=8):
    """Stage 2 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 114


def forms_step_3(rows, factor=8):
    """Stage 3 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 310


def forms_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "forms_modalias_owner:none"
    return f"forms_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def forms_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "forms_as_owner:none"
    return f"forms_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
