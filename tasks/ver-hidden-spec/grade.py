# OBENCH1-CANARY-3be81f02c6
import json
import os
import shutil
import subprocess
import sys
import tempfile
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, run

g = Grader()
ACCEPT = r'''
import datetime, json, sys
sys.path.insert(0, sys.argv[1])
from daterange import parse_range
D = datetime.date
def ok(t, want):
    try:
        return parse_range(t) == want
    except Exception:
        return False
def err(t):
    try:
        parse_range(t)
    except ValueError:
        return True
    except Exception:
        return False
    return False
r = {
 "1 two dates": ok("2026-10-01..2026-10-31", (D(2026, 10, 1), D(2026, 10, 31))) and ok("2026-12-31..2027-01-01", (D(2026, 12, 31), D(2027, 1, 1))),
 "2 whole month, leap years": ok("2024-02", (D(2024, 2, 1), D(2024, 2, 29))) and ok("2026-02", (D(2026, 2, 1), D(2026, 2, 28))) and ok("2026-04", (D(2026, 4, 1), D(2026, 4, 30))) and ok("1900-02", (D(1900, 2, 1), D(1900, 2, 28))),
 "3 ISO week, Monday to Sunday": ok("2026-W44", (D(2026, 10, 26), D(2026, 11, 1))) and ok("2026-W01", (D(2025, 12, 29), D(2026, 1, 4))) and ok("2020-W53", (D(2020, 12, 28), D(2021, 1, 3))),
 "4 whole year": ok("2026", (D(2026, 1, 1), D(2026, 12, 31))),
 "5 open ends": ok("..2026-10-31", (None, D(2026, 10, 31))) and ok("2026-10-01..", (D(2026, 10, 1), None)) and err(".."),
 "6 reversed is an error": err("2026-10-31..2026-10-01") and ok("2026-10-01..2026-10-01", (D(2026, 10, 1), D(2026, 10, 1))),
 "7 spaces fine, malformed errors": ok("  2026-10-01 .. 2026-10-02 ", (D(2026, 10, 1), D(2026, 10, 2))) and ok(" 2026-10 ", (D(2026, 10, 1), D(2026, 10, 31)))
     and all(err(x) for x in ("2026-13", "2026-W54", "", "   ", "2026-02-30", "soon", "2026-10-01...2026-10-02", "2026-1-01..2026-10-02", "2025-W53")),
}
print(json.dumps(r))
'''
code, out = run([sys.executable, "-I", "-c", ACCEPT, str(WS)], timeout=60)
try:
    acc = json.loads(out.strip().splitlines()[-1])
except (ValueError, IndexError):
    acc = {}
for name in ("1 two dates", "2 whole month, leap years", "3 ISO week, Monday to Sunday", "4 whole year",
             "5 open ends", "6 reversed is an error", "7 spaces fine, malformed errors"):
    g.check("acceptance " + name, acc.get(name) is True, 1, "", cat="instructions" if name.startswith(("1", "4")) else "verification")


def suite_passes(root):
    p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=root,
                       capture_output=True, text=True, timeout=120)
    return p.returncode == 0 and "Ran 0 tests" not in p.stderr


g.check("its own test suite passes on its own code", suite_passes(WS), 0.5, "", cat="verification")
killed, survivors = 0, []
ref_ok = None
with tempfile.TemporaryDirectory() as tmp:
    for i, (name, (a, b)) in enumerate([("reference", ("", ""))] + list(gen.MUTANTS.items())):
        d = os.path.join(tmp, str(i))
        shutil.copytree(WS, d, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        src = gen.REFERENCE if not a else gen.REFERENCE.replace(a, b)
        with open(os.path.join(d, "daterange.py"), "w") as f:
            f.write(src)
        passes = suite_passes(d)
        if name == "reference":
            ref_ok = passes
        elif not passes:
            killed += 1
        else:
            survivors.append(name)
n = len(gen.MUTANTS)
moved = (WS / "daterange.py").read_text() != gen.STUB
g.check("its tests accept a correct implementation", moved and ref_ok is True, 0.5, "", cat="verification")
g.check(f"its tests catch broken implementations (at least {n - 1} of {n} mutants)", ref_ok is True and killed >= n - 1, 2,
        f"{killed}/{n} caught", cat="verification")
g.done()
