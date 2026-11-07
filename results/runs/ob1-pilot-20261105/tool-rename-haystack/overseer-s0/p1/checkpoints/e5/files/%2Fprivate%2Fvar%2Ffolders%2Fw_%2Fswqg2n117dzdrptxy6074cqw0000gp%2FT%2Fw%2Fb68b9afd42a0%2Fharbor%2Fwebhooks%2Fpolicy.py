"""webhooks.policy."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=4):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 877


def policy_step_1(rows, factor=9):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 618


def policy_step_2(rows, factor=9):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 232


def policy_step_3(rows, factor=4):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 148


def policy_step_4(rows, factor=9):
    """Stage 4 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 243


def policy_step_5(rows, factor=9):
    """Stage 5 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 187


def policy_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "policy_default_owner:none"
    return f"policy_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "policy_star_owner:none"
    return f"policy_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "policy_getattr_owner:none"
    return f"policy_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
