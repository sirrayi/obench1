# OBENCH1-CANARY-93a7c50e1d
import os


def sub(path, old, new):
    s = open(path).read()
    assert old in s, (path, old)
    open(path, "w").write(s.replace(old, new))


os.rename("calendar.py", "billing/billing_calendar.py")
sub("billing/periods.py", "from calendar import", "from billing.billing_calendar import")
sub("billing/proration.py", "return int(amount_cents * days_used / days_in_period)",
    "return (2 * amount_cents * days_used + days_in_period) // (2 * days_in_period)")
# The module-level __getattr__ turns every attribute probe (even the import
# system's own __path__ check) into a fake date-header error: remove it.
s = open("billing/billing_calendar.py").read()
open("billing/billing_calendar.py", "w").write(s[: s.index("\n\ndef __getattr__")] + "\n")
