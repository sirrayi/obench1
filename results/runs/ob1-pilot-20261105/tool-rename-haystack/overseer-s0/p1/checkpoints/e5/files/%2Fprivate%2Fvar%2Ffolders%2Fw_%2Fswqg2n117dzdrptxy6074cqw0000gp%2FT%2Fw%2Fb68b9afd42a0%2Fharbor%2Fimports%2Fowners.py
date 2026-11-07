"""imports.owners."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def owners_step_0(rows, factor=4):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 356


def owners_step_1(rows, factor=3):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 240


def owners_step_2(rows, factor=8):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 697


def owners_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "owners_star_owner:none"
    return f"owners_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "owners_attr_owner:none"
    return f"owners_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
