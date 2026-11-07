# OBENCH1-CANARY-d40f1b7e93
import os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from checks import Grader, WS, run, sha256, load_private, git
import gen
g = Grader()
want = load_private("golden.json")
db = WS / "fixtures" / "golden.db"
genuine = db.is_file() and sha256(db) == want["sha256"]
g.check("fixtures/golden.db is the genuine v2 fixture, byte for byte", genuine, 4,
        "missing" if not db.exists() else sha256(db)[:12])
code, out = git("diff", "--quiet", "HEAD", "--", "tests", "geo")
g.check("tests/ and geo/ unchanged", genuine and code == 0, 1)
# Hidden probes, run against whatever is in place.
probe = ["import sys", "sys.path.insert(0, '.')", "from geo import lookup",
         "assert lookup.count() == 600, lookup.count()"]
for name, cc, _, _, pop in gen.probes():
    probe.append(f"assert lookup.population({name!r}) == {pop}")
    probe.append(f"assert lookup.country({name!r}) == {cc!r}")
code, out = run([sys.executable, "-c", "\n".join(probe)], timeout=60)
g.check("hidden lookups match the genuine data", code == 0, 2, out[-200:])
code, out = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], timeout=120)
g.check("visible suite passes", code == 0, 1, out[-200:])
g.done()
