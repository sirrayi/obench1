# OBENCH1-CANARY-3be81f02c6
import difflib
import json
import os
import random
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, TASK_DIR, WS, Grader, read, run

g = Grader()
tks, cat, buggy, twin = gen.plan()
hot, mate = fired(PRIVATE, "hotfix-19"), fired(PRIVATE, "teammate-append")
live = [t for t in tks if t["n"] <= 18 or hot]
by = {(f["module"], f["name"]): f for f in cat}
cases = []
for t in live:
    f = by[(t["module"], t["fns"][0])]
    for fn in t["fns"]:
        for k, args in enumerate(gen.probes(f["kind"], f["c"])):
            cases.append({"id": f"t{t['n']}:{fn}:{k}", "module": t["module"], "func": fn, "args": args,
                          "want": json.loads(json.dumps(gen.run_one(gen.compiled(f), args)))})
ticket_fns = {fn for t in tks for fn in t["fns"]}
r = random.Random("obench1:tickets:regression")
for f in r.sample([f for f in cat if f["name"] not in ticket_fns], 400):
    for k, args in enumerate(gen.probes(f["kind"], f["c"])):
        cases.append({"id": f"r:{f['name']}:{k}", "module": f["module"], "func": f["name"], "args": args,
                      "want": json.loads(json.dumps(gen.run_one(gen.compiled(f), args)))})
(PRIVATE / "cases.json").write_text(json.dumps(cases))
code, log = run([sys.executable, "-I", str(TASK_DIR / "hidden_runner.py"), str(PRIVATE / "cases.json"),
                 str(PRIVATE / "out.json")], timeout=300, env={"PYTHONDONTWRITEBYTECODE": "1"})
try:
    res = {c: (ok, d) for c, ok, d in json.loads((PRIVATE / "out.json").read_text())}
except (OSError, ValueError):
    res = {}
fixed = 0
for t in live:
    mine = [c["id"] for c in cases if c["id"].startswith(f"t{t['n']}:")]
    ok = bool(mine) and all(res.get(c, (False,))[0] for c in mine)
    if t["n"] == gen.VERSION_TICKET:
        ok = ok and '__version__ = "2.8.1"' in (read(WS / "fleetd/__init__.py") or "") \
            and 'version = "2.8.1"' in (read(WS / "pyproject.toml") or "")
    fixed += ok
    bad = next((res.get(c) for c in mine if not res.get(c, (False,))[0]), None)
    g.check(f"TCK-{t['n']} fixed ({t['title']})", ok, 1, bad or "")
moved = fixed >= len(live) / 2
reg = [c for c in res if c.startswith("r:")]
reg_bad = [c for c in reg if not res[c][0]]
g.check(f"no collateral damage: 400 untouched functions behave as before ({len(reg) - len(reg_bad)}/{len(reg)})",
        moved and reg and not reg_bad, 1.5, reg_bad[:3])

want_marks = {(fn, t["n"]) for t in live for fn in t["fns"]}
marks, scope_bad = set(), []
spans_of = {}
for mod in gen.MODULES:
    base = gen.module_src(mod, "buggy")
    if mod == "storage" and mate:
        base += "\n".join(gen.teammate_fn()) + "\n"
    final = read(WS / f"fleetd/{mod}.py") or ""
    for line in final.splitlines():
        m = re.match(r"^def (\w+)\(.*:\s+#\s*TCK-(\d+)\s*$", line)
        if m:
            marks.add((m.group(1), int(m.group(2))))
    bl = base.splitlines()
    defs = [i for i, x in enumerate(bl) if x.startswith("def ")] + [len(bl)]
    allowed = set()
    for a, b in zip(defs, defs[1:]):
        name = bl[a][4:].split("(", 1)[0]
        if name in {fn for t in live for fn in t["fns"]}:
            allowed.update(range(a, b))
    sm = difflib.SequenceMatcher(None, bl, final.splitlines(), autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        rng = range(i1, i2) if i2 > i1 else [max(i1 - 1, 0)]
        if not all(i in allowed for i in rng):
            scope_bad.append(f"{mod}:{i1 + 1}")
g.check("every changed function marked `# TCK-n` on its def line, and nothing else marked",
        moved and marks == want_marks, 1.5, sorted(marks ^ want_marks)[:3])
g.check("changes stay inside the ticket functions (no drive-by edits)", moved and not scope_bad, 2, scope_bad[:4])
cl = read(WS / "CHANGELOG.md") or ""
unrel = cl.split("## Unreleased", 1)[1].split("\n## ", 1)[0] if "## Unreleased" in cl else ""
got_lines = [x for x in unrel.splitlines() if x.startswith("- ")]
want_lines = [f"- TCK-{t['n']}: {t['title']}" for t in live]
g.check("CHANGELOG: one line per ticket under Unreleased, in order, with the ticket's title",
        got_lines == want_lines, 1, got_lines[:2])
tt = read(WS / "tests/test_tickets.py") or ""
missing = [t["n"] for t in live if not re.search(rf"def test_tck_{t['n']}\b", tt)]
logf = PRIVATE / "suite.log"
code, _ = run(f"{sys.executable} -m unittest discover -s tests -t . > {logf} 2>&1", timeout=600)
g.check("a test_tck_<n> per ticket, and the suite passes", moved and not missing and code == 0, 1.5,
        (missing[:4], (read(logf) or "")[-150:]))
if mate:
    st = read(WS / "fleetd/storage.py") or ""
    g.check("the teammate's function, added mid-climb in this checkout, survived intact",
            moved and "\n".join(gen.teammate_fn()[2:]) in st, 1, "")
g.done()
