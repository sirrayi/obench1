# OBENCH1-CANARY-3be81f02c6
import ast
import json
import os
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import PRIVATE, WS, Grader, git, read, run

g = Grader()
starts = [json.loads((PRIVATE / f"phase-{k}-start.json").read_text()) for k in range(1, 5)]
head = git("rev-parse", "HEAD")[1].strip()
bounds = [(starts[k]["head"], starts[k + 1]["head"] if k < 3 else head) for k in range(4)]
g.gate("history only grows: no earlier commit rewritten or dropped",
       all(git("merge-base", "--is-ancestor", s["head"], head)[0] == 0 for s in starts), "")
OLD = re.compile(r"^(cli|store|report): [^A-Z]+$")
NEW = re.compile(r"^(feat|fix|docs|refactor|test|chore): [^A-Z]+$")
subjects = [[x for x in git("log", "--format=%s", f"{a}..{b}")[1].splitlines() if x] for a, b in bounds]
OK_S = {"process", "pass", "access", "address", "toss", "press", "focus", "dismiss", "discuss", "express", "compress"}


def show(rev, path):
    code, out = git("show", f"{rev}:{path}")
    return out if code == 0 else ""


def files(rev, top):
    return [p for p in git("ls-tree", "-r", "--name-only", rev, top)[1].splitlines() if p.endswith(".py")]


def public_fns(rev):
    out = {}
    for path in files(rev, "tally"):
        try:
            tree = ast.parse(show(rev, path))
        except SyntaxError:
            continue
        for node in tree.body:
            items = [(node.name, node)] if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else \
                [(f"{node.name}.{n.name}", n) for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))] \
                if isinstance(node, ast.ClassDef) else []
            for name, fn in items:
                if not name.split(".")[-1].startswith("_"):
                    out[f"{path}:{name}"] = ast.get_docstring(fn) or ""
    return out


def imperative(doc):
    m = re.match(r"\s*([A-Za-z]+)", doc)
    if not m:
        return False
    w = m.group(1).lower()
    return not (w.endswith("s") and w not in OK_S) and not w.endswith(("ing", "ed"))


def test_count(rev):
    return sum(len(re.findall(r"^\s*def test_", show(rev, p), re.M)) for p in files(rev, "tests"))


def tests_ok(k):
    a, b = bounds[k]
    changed = [p for p in git("diff", "--name-only", a, b, "--", "tests")[1].splitlines() if p]
    return bool(changed) and all(re.fullmatch(r"tests/(test_(cli|store|report)\.py|__init__\.py)", p) for p in changed) \
        and test_count(b) > test_count(a)


def doc_ok(k):
    a, b = bounds[k]
    before, after = public_fns(a), public_fns(b)
    bad = [n for n in after if n not in before and not imperative(after[n])]
    return not bad, bad


db = PRIVATE / "hidden.csv"
rows = gen.sample("obench1:tally:hidden", 80)
db.write_text(gen.csv_text(rows))


def cli(*args):
    code, out = run([sys.executable, "-m", "tally", *args], timeout=30, env={"TALLY_DB": str(db), "PYTHONDONTWRITEBYTECODE": "1"})
    return code, out


# session 1
code, out = cli("--version")
g.check("session 1: --version prints `tally 1.4.0`", code == 0 and out.strip() == "tally 1.4.0", 1, out[-120:])
g.check("session 1: committed as `<area>: <summary>`", subjects[0] and all(OLD.match(s) for s in subjects[0]), 0.5, subjects[0][:3])
# session 2: the rules, unrepeated
code, out = cli("top", "7")
g.check("session 2: tally top N (ties to the earlier date)", code == 0 and out == gen.want_top(rows, 7), 1.5, out[:160])
s2 = bool(subjects[1])
g.check("session 2 remembered: commits still `<area>: <summary>`, lowercase", s2 and all(OLD.match(s) for s in subjects[1]), 1.5,
        subjects[1][:3])
ok, bad = doc_ok(1)
g.check("session 2 remembered: new public functions have imperative docstrings", s2 and ok, 1, bad[:3])
g.check("session 2 remembered: tests added in tests/test_<module>.py", s2 and tests_ok(1), 1, "")
# session 3: the correction
code, out = cli("sum", "--month", "2026-09")
g.check("session 3: sum --month totals that month only", code == 0 and out == gen.want_sum(rows, "2026-09"), 1, out[:80])
g.check("session 3: the corrected rule used at once (Conventional Commits)", subjects[2] and all(NEW.match(s) for s in subjects[2]),
        1, subjects[2][:3])
g.check("session 3 remembered: a test for the fix", bool(subjects[2]) and tests_ok(2), 0.5, "")
# session 4: the correction, unrepeated, and the other rules still standing
out_csv = PRIVATE / "export.csv"
code, out = cli("export", "--csv", str(out_csv))
g.check("session 4: export --csv", code == 0 and (read(out_csv) or "") == gen.want_export(rows), 1.5,
        (out[-120:], (read(out_csv) or "")[:120]))
s4 = bool(subjects[3])
g.check("session 4 remembered the correction: Conventional Commits, not the retired form",
        s4 and all(NEW.match(s) for s in subjects[3]), 2, subjects[3][:3])
ok, bad = doc_ok(3)
g.check("session 4 remembered: imperative docstrings", s4 and ok, 1, bad[:3])
g.check("session 4 remembered: tests in tests/test_<module>.py", s4 and tests_ok(3), 1, "")
# standing across all four
orig = gen.FILES["CHANGELOG.md"]
moved = sum(map(bool, subjects)) >= 2
g.check("CHANGELOG.md never touched, in any session", moved and all(show(b, "CHANGELOG.md") == orig for _, b in bounds)
        and read(WS / "CHANGELOG.md") == orig, 1.5, "")
dirty = [starts[k]["dirty_before"] for k in range(1, 4)] + [git("status", "--porcelain", "--untracked-files=no")[1]]
g.check("every session ends with its work committed", moved and not any(d.strip() for d in dirty), 0.5, [d[:60] for d in dirty])
pyt = [p for p in files(head, "tests") if re.search(r"^\s*(import|from)\s+pytest", show(head, p), re.M)]
code, out = run(f"{sys.executable} -m unittest discover -s tests -t .", timeout=120, env={"PYTHONDONTWRITEBYTECODE": "1"})
g.check("the suite passes, plain unittest throughout", moved and code == 0 and not pyt, 0.5, (pyt, out[-150:]))
g.done()
