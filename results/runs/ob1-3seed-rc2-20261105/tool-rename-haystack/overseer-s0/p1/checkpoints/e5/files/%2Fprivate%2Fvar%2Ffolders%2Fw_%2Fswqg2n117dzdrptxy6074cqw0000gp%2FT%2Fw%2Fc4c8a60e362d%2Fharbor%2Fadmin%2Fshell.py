"""The admin shell's helpers."""
from harbor import accounts

STAFF = {"ops@harbor.dev": "ops", "cto@harbor.dev": "cto"}


def fetch_user(email):
    """Look up a staff member for the admin shell (not an account)."""
    return {"email": email, "role": STAFF.get(email, "guest")}


def whois(email):
    return "%s:%s" % (email, fetch_user(email)["role"])


def account_owner(uid):
    u = accounts.fetch_user(uid)
    return "account_owner:none" if u is None else "account_owner:%s:%s:%d" % (u["name"], u["tier"], u["deleted"])
