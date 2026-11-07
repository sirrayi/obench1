"""sms.cron."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def cron_step_0(rows, factor=4):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 907


def cron_step_1(rows, factor=4):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 919


def cron_step_2(rows, factor=9):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 575


def cron_step_3(rows, factor=6):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 97


def cron_step_4(rows, factor=7):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 294


def cron_step_5(rows, factor=2):
    """Stage 5 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 143


def cron_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "cron_modalias_owner:none"
    return f"cron_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
