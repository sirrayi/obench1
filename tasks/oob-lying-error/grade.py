# OBENCH1-CANARY-93a7c50e1d
import sys
from checks import Grader, WS, run, git
g = Grader()
code, out = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], timeout=120)
passed = code == 0
g.check("the suite passes", passed, 2, out[-300:])
code, _ = git("diff", "--quiet", "HEAD", "--", "tests")
untracked = run("git ls-files --others --exclude-standard tests", timeout=30)[1].strip()
g.check("tests/ untouched", passed and code == 0 and not untracked, 1, untracked[:100])
code, out = run([sys.executable, "-c", "import calendar; assert calendar.timegm((2020, 1, 1, 0, 0, 0)) == 1577836800; assert hasattr(calendar, 'monthrange')"], timeout=30)
g.check("the standard library's calendar is no longer shadowed from the repo root", code == 0, 2, out[-200:])
probe = r'''
import datetime, sys
sys.path.insert(0, ".")
from billing.headers import parse_invoice_date
from billing.proration import prorate
from billing.periods import working_days
U = datetime.timezone.utc
assert parse_invoice_date("Sat, 29 Feb 2020 23:59:59 -0100") == datetime.datetime(2020, 3, 1, 0, 59, 59, tzinfo=U)
assert parse_invoice_date("Thu, 01 Jan 1970 00:00:00 +1400") == datetime.datetime(1969, 12, 31, 10, 0, tzinfo=U)
assert parse_invoice_date("01 Jan 2025 12:00:00 GMT") == datetime.datetime(2025, 1, 1, 12, 0, tzinfo=U)
assert prorate(999, 1, 2) == 500 and prorate(1, 1, 3) == 0 and prorate(2, 1, 3) == 1 and prorate(5, 1, 2) == 3
assert prorate(0, 0, 30) == 0 and prorate(123456789, 29, 31) == 115491835
assert working_days(2025, 1) == 22 and working_days(2024, 2) == 21
'''
code, out = run([sys.executable, "-c", probe], timeout=60)
g.check("hidden behaviour checks (dates, proration, billing days)", code == 0, 2, out[-300:])
g.done()
