"""plans.models."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def models_step_0(rows, factor=8):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 921


def models_step_1(rows, factor=7):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 136


def models_step_2(rows, factor=8):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 987


def models_step_3(rows, factor=7):
    """Stage 3 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 473


def models_step_4(rows, factor=5):
    """Stage 4 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 520


def models_step_5(rows, factor=3):
    """Stage 5 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 830


def models_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "models_direct_owner:none"
    return f"models_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_timer():
    return telemetry.timer("accounts.fetch_user.calls")
