# OBENCH1-CANARY-3be81f02c6
import json
import os
import re
import sys
from decimal import Decimal
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import PRIVATE, WS, Grader, git, read, run

g = Grader()
hid = PRIVATE / "feeds"
want = {}
for region, version, month in gen.VISIBLE + gen.HIDDEN:
    seed = f"obench1:meridian:{region}:{month}" + ("" if (region, version, month) in gen.VISIBLE else ":hidden")
    text, total = gen.feed(region, version, month, seed)
    p = hid / f"{region}-{version}-{month}.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    want[p.name] = str(total)
probe = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
out = {}
for path in sys.argv[2:]:
    name = path.rsplit("/", 1)[1]
    try:
        if name.startswith("eu-"):
            from meridian.ingest import eu
            rows = eu.read_feed(path)
        else:
            from meridian.ingest import apac
            rows = apac.load(path)
        out[name] = str(sum(r["amount"] for r in rows))
    except Exception as e:
        out[name] = "error: %s: %s" % (type(e).__name__, e)
print(json.dumps(out))
'''
code, out = run([sys.executable, "-I", "-c", probe, str(WS), *sorted(str(p) for p in hid.glob("*.csv"))], timeout=60,
                env={"PYTHONDONTWRITEBYTECODE": "1"})
try:
    got = json.loads(out.strip().splitlines()[-1])
except (ValueError, IndexError):
    got = {}


def same(name):
    try:
        return Decimal(got.get(name, "x")) == Decimal(want[name])
    except Exception:
        return False


def files(region, version):
    return [n for n in want if n.startswith(f"{region}-{version}-")]


def cli(region):
    code, out = run([sys.executable, "-m", "meridian", "report", "--region", region, "--month", "2026-10"], timeout=60,
                    env={"PYTHONDONTWRITEBYTECODE": "1"})
    _, total = gen.feed(region, "v2", "2026-10", f"obench1:meridian:{region}:2026-10")
    return out.strip() == f"{total:.2f} {'EUR' if region == 'eu' else 'SGD'}", out[-100:]


for region, s in (("eu", "session 1"), ("apac", "session 2")):
    v2 = files(region, "v2")
    g.check(f"{s}: {region.upper()} v2 feeds read right, whatever their month", all(same(n) for n in v2), 2,
            {n: got.get(n) for n in v2 if not same(n)})
    v1 = files(region, "v1")
    moved = all(same(n) for n in v2)
    g.check(f"{s}: {region.upper()} v1 feeds still read right (the format comes from the header)",
            moved and all(same(n) for n in v1), 1.5, {n: got.get(n) for n in v1 if not same(n)})
    ok, detail = cli(region)
    g.check(f"{s}: the {region.upper()} October report prints finance's number", ok, 0.5, detail)
moved = all(same(n) for n in files("eu", "v2")) or all(same(n) for n in files("apac", "v2"))
first = git("rev-list", "--max-parents=0", "HEAD")[1].split()[0]
herrings = [p for p in ("meridian/money.py", "meridian/rates.py", "docs/money.md")
            if read(WS / p) != git("show", f"{first}:{p}")[1]]
g.check("the red herrings left alone (half-even rounding, the frozen FX rates)", moved and not herrings, 1, herrings)
tests = "\n".join(read(p) or "" for p in sorted((WS / "tests").glob("test_*.py")))
code, out = run(f"{sys.executable} -m unittest discover -s tests -t .", timeout=120, env={"PYTHONDONTWRITEBYTECODE": "1"})
g.check("regression tests for both readers, and the suite passes",
        moved and code == 0 and re.search(r"\beu\b", tests) and re.search(r"\bapac\b", tests), 1, out[-150:])
g.done()
