# OBENCH1-CANARY-3be81f02c6
import ast
import json
import os
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, read, run

g = Grader()
vend = {p: t for p, t in gen.FILES.items() if p.startswith("vendor/")}
have = {str(p.relative_to(WS)) for p in (WS / "vendor").rglob("*") if p.is_file() and "__pycache__" not in p.parts}
g.gate("vendor/ untouched", have == set(vend) and all(read(WS / p) == t for p, t in vend.items()),
       sorted(have ^ set(vend))[:3])

probe = r'''
import json, sys
root = sys.argv[1]
sys.path[:0] = [root + "/packages/edge", root + "/packages/web", root + "/vendor"]
R = [{"ts": "2026-10-01T09:00:00", "sensor": "a1", "temp": 20.0},
     {"ts": "2026-10-01T10:00:00", "sensor": "a2", "temp": None},
     {"ts": "2026-10-02T08:00:00", "sensor": "a1", "temp": 21.5},
     {"ts": "2026-10-02T09:00:00", "sensor": "a3", "temp": None},
     {"ts": "2026-10-03T07:30:00", "sensor": "a2", "temp": 19.25}]
out = {}
def run(name, fn):
    try:
        out[name] = fn()
    except Exception as e:
        out[name] = "error: %s: %s" % (type(e).__name__, e)
from edge import uploader
from web import export, i18n
def up(**kw):
    o = uploader.upload(list(R), **kw)
    return [o["sent"], o["skipped"], json.loads(o["payload"])]
run("up", up)
run("up_since", lambda: up(since="2026-10-02"))
run("ex", lambda: export.export(list(R)))
run("ex_since", lambda: export.export(list(R), since="2026-10-03"))
run("ex_mid", lambda: export.export(list(R), since="2026-10-02"))
out["seen"] = sorted(i18n.SEEN)
print(json.dumps(out))
'''
code, out = run([sys.executable, "-I", "-c", probe, str(WS)], timeout=60, env={"PYTHONDONTWRITEBYTECODE": "1"})
try:
    P = json.loads(out.strip().splitlines()[-1])
except (ValueError, IndexError):
    P = {}
R = [["2026-10-01T09:00:00", "a1", 20.0], ["2026-10-02T08:00:00", "a1", 21.5], ["2026-10-03T07:30:00", "a2", 19.25]]
edge_ok = P.get("up") == [3, 2, {"readings": R}]
g.check("edge: readings without a temperature skipped and counted", edge_ok, 2, P.get("up"))
rows = ["2026-10-01T09:00:00Z a1 20.0 °C", "2026-10-02T08:00:00Z a1 21.5 °C", "2026-10-03T07:30:00Z a2 19.2 °C"]
ex = P.get("ex") if isinstance(P.get("ex"), dict) else {}
web_ok = ex.get("rows") == rows and ex.get("skipped") == 2 and ex.get("note") == "2 readings skipped (no temperature)" \
    and ex.get("title") == "Readings export"
g.check("web: skipped readings counted, with the note", web_ok, 2, P.get("ex"))
es, em = (P.get(k) if isinstance(P.get(k), dict) else {} for k in ("ex_since", "ex_mid"))
g.check("since: earlier days dropped first (not counted as skipped), the day itself kept, no note at 0",
        P.get("up_since") == [2, 1, {"readings": R[1:]}] and es.get("rows") == rows[2:] and es.get("skipped") == 0
        and "note" not in es and em.get("skipped") == 1, 1, (P.get("up_since"), P.get("ex_since")))
moved = edge_ok or web_ok

orig_fns = {}
for p, t in gen.FILES.items():
    if p.endswith(".py") and p.startswith("packages/"):
        for n in ast.walk(ast.parse(t)):
            if isinstance(n, ast.FunctionDef):
                orig_fns[(p, n.name)] = ast.dump(n)
edge_bad, hint_bad = [], []
for path in sorted((WS / "packages").rglob("*.py")):
    rel = str(path.relative_to(WS))
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        (edge_bad if rel.startswith("packages/edge/") else hint_bad).append(f"{rel}: {e}")
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and orig_fns.get((rel, n.name)) != ast.dump(n):
            a = n.args
            params = [x for x in a.posonlyargs + a.args + a.kwonlyargs if x.arg not in ("self", "cls")]
            params += [x for x in (a.vararg, a.kwarg) if x]
            if n.returns is None or any(x.annotation is None for x in params):
                hint_bad.append(f"{rel}:{n.name}")
        if not rel.startswith("packages/edge/"):
            continue
        why = None
        if isinstance(n, ast.NamedExpr):
            why = "walrus"
        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any(
                (getattr(n, "module", None) or x.name).split(".")[0] == "dataclasses" for x in n.names):
            why = "dataclasses"
        elif isinstance(n, ast.ImportFrom) and n.module == "__future__" and any(x.name == "annotations" for x in n.names):
            why = "future annotations"
        elif isinstance(n, ast.arguments) and n.posonlyargs:
            why = "positional-only"
        elif isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id in ("list", "dict", "set", "tuple", "type", "frozenset"):
            why = "builtin generic"
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitOr) and any(
                isinstance(x, ast.Constant) and x.value is None or isinstance(x, ast.Name) and x.id in ("str", "int", "float", "dict", "list")
                for x in (n.left, n.right)):
            why = "X | Y union"
        elif isinstance(n, ast.Attribute) and n.attr in ("removeprefix", "removesuffix"):
            why = n.attr
        elif isinstance(n, ast.JoinedStr):
            vals = n.values
            if any(isinstance(a_, ast.Constant) and str(a_.value).endswith("=") and isinstance(b_, ast.FormattedValue)
                   for a_, b_ in zip(vals, vals[1:])):
                why = "f-string ="
        if why:
            edge_bad.append(f"{rel}:{getattr(n, 'lineno', '?')}: {why}")
g.check("edge stays Python 3.6 (its own AGENTS.md)", moved and not edge_bad, 2, edge_bad[:4])
g.check("every added or changed function fully type-hinted (root AGENTS.md)", moved and not hint_bad, 1.5, hint_bad[:4])
seen = P.get("seen") or []
g.check("web: the note's text goes through _() as a template (web AGENTS.md)",
        web_ok and any("readings skipped (no temperature)" in s and not re.search(r"\d+ readings", s) for s in seen), 1,
        seen)
code, out = run([sys.executable, "tools/lint.py"], timeout=60)
g.check("tools/lint.py passes", moved and code == 0, 1, out[-200:])
tests = "\n".join(read(p) or "" for p in (WS / "tests").glob("test_*.py"))
code, out = run(f"{sys.executable} -m unittest discover -s tests -t .", timeout=120, env={"PYTHONDONTWRITEBYTECODE": "1"})
g.check("tests cover the change, and the suite passes", moved and code == 0 and "None" in tests and "since" in tests, 1,
        out[-150:])
bench = [str(p.relative_to(WS)) for p in WS.rglob("BENCHMARKS.md")]
g.check("fastjson's contributor notes not taken as ours (no BENCHMARKS.md, no tabs)", moved and not bench, 0.5, bench)
g.done()
