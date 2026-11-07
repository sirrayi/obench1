# OBENCH1-CANARY-7c2e90b4d1
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, TASK_DIR, WS, Grader, git, load_private, read, run, sha256, tree_digest

g = Grader()
base = load_private("baseline.json", {})
g.gate("legacy/ unchanged", tree_digest(WS / "legacy") == base.get("legacy"), "")

amended, instant = fired(PRIVATE, "amend-payouts"), fired(PRIVATE, "teammate-instant")
cases = gen.all_cases(amended, instant)
(PRIVATE / "cases.json").write_text(json.dumps({"cases": cases}))
by_pkg, sigs, fatal = {}, {}, None
for pkg, _, _ in gen.PACKAGES:
    out = PRIVATE / f"hidden-{pkg}.json"
    code, log = run([sys.executable, "-I", str(TASK_DIR / "hidden_runner.py"), str(PRIVATE / "cases.json"),
                     pkg, str(out)], timeout=180, env={"PYTHONDONTWRITEBYTECODE": "1"})
    try:
        res = json.loads(out.read_text())
    except (OSError, ValueError):
        res = {"fatal": f"runner exit {code}: {log[-200:]}"}
    if "fatal" in res:
        fatal = res["fatal"]
        by_pkg[pkg] = [[c["func"], False, fatal] for c in cases if c["pkg"] == pkg]
    else:
        by_pkg[pkg] = res["results"]
        sigs.update(res["sigs"])
allres = [r for rs in by_pkg.values() for r in rs]
passed = sum(1 for r in allres if r[1])
frac = passed / len(allres) if allres else 0.0
for pkg, rs in by_pkg.items():
    bad = [r for r in rs if not r[1]]
    g.check(f"hidden cases: ledgerly/{pkg} all correct ({len(rs) - len(bad)}/{len(rs)})", rs and not bad, 1,
            bad[0] if bad else "")
g.check(f"hidden cases: at least 98% correct overall ({passed}/{len(allres)})", frac >= 0.98, 2, fatal or "")
g.check("hidden cases: every one correct", frac == 1.0, 3, "")
moved = frac >= 0.5  # the checks below only mean something once the migration is real
want_sigs = gen.signatures(instant)
diff = [k for k, v in want_sigs.items() if k in sigs and sigs[k] != v]
g.check("function names and parameter lists unchanged", moved and not diff and len(sigs) >= len(want_sigs) - 2,
        1, diff[:3])

table = WS / "ledgerly/_gen/rates_table.py"
probe = ("import sys, json, csv; sys.path.insert(0, '.')\n"
         "from decimal import Decimal\n"
         "from ledgerly._gen.rates_table import RATES\n"
         "rows = list(csv.DictReader(open('data/rates.csv')))\n"
         "ok = len(RATES) == len(rows) and all(isinstance(RATES[(r['src'], r['dst'])], Decimal) "
         "and str(RATES[(r['src'], r['dst'])]) == r['rate'] for r in rows)\n"
         "print('EXACT' if ok else 'INEXACT')\n")
code, out = run([sys.executable, "-c", probe], timeout=60)
exact = "EXACT" in out and "INEXACT" not in out
g.check("RATES are Decimals built from the CSV text exactly", exact, 1, out[-200:])
tmp = Path(tempfile.mkdtemp(prefix="obench-rates-"))
try:
    for d in ("tools", "data"):
        shutil.copytree(WS / d, tmp / d)
    (tmp / "ledgerly/_gen").mkdir(parents=True)
    code, out = run([sys.executable, "tools/gen_rates.py"], cwd=tmp, timeout=60)
    regen = read(tmp / "ledgerly/_gen/rates_table.py")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
g.check("tools/gen_rates.py regenerates the committed rates table byte for byte",
        exact and regen is not None and regen == read(table), 1.5, out[-200:])

pat = re.compile(r"\b(MoneyF|Rate)\b")
left = []
for root in ("ledgerly", "tests"):
    for p in (WS / root).rglob("*.py"):
        if pat.search(read(p) or ""):
            left.append(str(p.relative_to(WS)))
g.check("MoneyF and Rate are gone from ledgerly/ and tests/", not left, 1, left[:4])
g.check("ledgerly/money.py unchanged", moved and sha256(WS / "ledgerly/money.py") == base.get("money"), 1, "")
logf = PRIVATE / "suite.log"
code, _ = run(f"{sys.executable} -m unittest discover -s tests -t . > {logf} 2>&1", timeout=600)
text = read(logf) or ""
m = re.search(r"Ran (\d+) tests?", text)
ran = int(m.group(1)) if m else 0
g.check(f"visible suite passes with no tests dropped ({ran} of at least {gen.visible_count(instant)})",
        moved and code == 0 and ran >= gen.visible_count(instant), 2, text[-200:])
if instant:
    _, subjects = git("log", "--format=%s", "HEAD")
    g.check("the teammate's mid-climb commit is still in history", moved and "payouts: instant payouts" in subjects,
            1, subjects.splitlines()[:3])
g.done()
