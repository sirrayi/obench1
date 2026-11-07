"""Late fees: who owes them, and how many accounts they could apply to."""
from harbor import accounts
from harbor.accounts import fetch_user_count

_OPTS = {"include_deleted": True}


def late_fee_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS)
    if u is None:
        return "late_fee_owner:none"
    return f"late_fee_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def late_fee_payer(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "late_fee_payer:none"
    return f"late_fee_payer:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def late_fee_population():
    return fetch_user_count()
