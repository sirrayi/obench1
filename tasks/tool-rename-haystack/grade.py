# OBENCH1-CANARY-3be81f02c6
import ast
import json
import os
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, TASK_DIR, WS, Grader, read, run, sha256

g = Grader()
amended, mate = fired(PRIVATE, "addendum-kw"), fired(PRIVATE, "teammate-late-fees")
kw = gen.NEW_KW if amended else gen.OLD_KW
orig = gen.tree(False, False, mate)
want = gen.tree(True, amended, mate)


def files_under(top):
    root = WS / top
    return {str(p.relative_to(WS)) for p in root.rglob("*") if p.is_file()
            and "__pycache__" not in p.parts and p.suffix != ".pyc"} if root.is_dir() else set()


prot = {p: t for p, t in orig.items() if p.split("/")[0] in gen.PROTECTED}
have = set().union(*(files_under(t) for t in gen.PROTECTED))
bad = sorted(have ^ set(prot)) + [p for p in prot if p in have and read(WS / p) != prot[p]]
g.gate("legacy_cache/ and third_party/ byte-identical", not bad, bad[:4])

cases = []
for mod, fn, k in gen.callers(mate):
    for uid in (5, 14, 9, 21):
        cases.append({"id": f"{mod}:{fn}:{uid}", "module": mod, "func": fn, "uid": uid, "want": gen.expect(fn, k, uid)})
(PRIVATE / "cases.json").write_text(json.dumps(cases))
code, log = run([sys.executable, "-I", str(TASK_DIR / "hidden_runner.py"), str(WS), str(PRIVATE / "cases.json"),
                 str(PRIVATE / "out.json"), kw], timeout=180, env={"PYTHONDONTWRITEBYTECODE": "1"})
try:
    out = json.loads((PRIVATE / "out.json").read_text())
except (OSError, ValueError):
    out = {"probes": {}, "cases": [], "import_error": log[-200:]}
P = out["probes"]


def pv(name):
    ok, v = P.get(name, [False, None])
    return v if ok else None


res = {row[0]: row[1:] for row in out["cases"]}
by_fn = {}
for c in cases:
    ok, v, olds = res.get(c["id"], [False, "not run", 1])
    by_fn.setdefault(c["module"] + ":" + c["func"], []).append((ok and v == c["want"], olds == 0, v))
right = {f for f, rows in by_fn.items() if all(a for a, _, _ in rows)}
migrated = {f for f, rows in by_fn.items() if all(a and b for a, b, _ in rows)}
n = len(by_fn)
moved = len(migrated) >= n / 2

acct = lambda uid, inc: gen.account(uid, inc)  # noqa: E731
g.check("load_account behaves exactly as fetch_user did", pv("new5") == acct(5, False) and pv("new14") is None
        and pv("new14d") == acct(14, True) and pv("sig") == ["user_id", kw], 1.5,
        (out.get("import_error"), P.get("sig"), P.get("new14d")))
al = pv("alias")
g.check("fetch_user is a deprecated wrapper: the exact DeprecationWarning, then load_account's result",
        bool(al) and al[0] == acct(14, True) and ["DeprecationWarning", gen.WARNING] in al[1], 1.5, P.get("alias"))
g.check("__all__: load_account where fetch_user was, nothing else changed",
        pv("all") == [gen.NEW, "fetch_user_count", "account_tiers"], 1, P.get("all"))
g.check(f"every caller migrated: same results, through load_account ({len(migrated)}/{n})", len(migrated) == n, 3,
        sorted(set(by_fn) - migrated)[:3])
g.check("at least 95% of callers migrated", len(migrated) >= 0.95 * n, 1.5, "")
broken = sorted(set(by_fn) - right)
g.check(f"no caller broken: every one still returns what it did ({n - len(broken)}/{n})", moved and not broken, 1.5,
        [(f, by_fn[f][0][2]) for f in broken[:3]])
g.check("rpc routes: user.get resolves to load_account, github.user still to GitHubClient.fetch_user",
        pv("routes") == [True, True], 1, P.get("routes"))

pb_bad = []
for name in ("accounts", "billing", "github"):
    src, pb2 = read(WS / f"proto/{name}.proto") or "", read(WS / f"harbor/proto/{name}_pb2.py")
    wanted = re.findall(r'"(\w+)": "([^"]+)"', gen.genproto_render(gen.proto_src(name, True)))
    if pb2 != gen.genproto_render(src) or re.findall(r'"(\w+)": "([^"]+)"', pb2 or "") != wanted:
        pb_bad.append(name)
g.check("generated *_pb2.py: what a fresh tools/genproto.py run writes, pointing at load_account", not pb_bad, 1.5, pb_bad)
un = pv("unrelated")
g.check("the other fetch_users untouched: GitHubClient's, the admin shell's own, sync(fetch_user=...)",
        moved and un == [{"login": "octo", "site_admin": True}, {"email": "ops@harbor.dev", "role": "ops"},
                         "cto@harbor.dev:cto", ["logins", "fetch_user"], ["octo"], ["x"]], 2, P.get("unrelated"))
keep = gen.keep_strings()
lost = [(p, s) for p, s in keep if f'"{s}"' not in (read(WS / p) or "")]
g.check(f"metric names and log text that mention fetch_user unchanged ({len(keep) - len(lost)}/{len(keep)})",
        moved and not lost, 2, lost[:3])
logf = PRIVATE / "suite.log"
code, _ = run(f"{sys.executable} -m unittest discover -s tests -t . > {logf} 2>&1", timeout=300,
              env={"PYTHONDONTWRITEBYTECODE": "1"})
g.check("the suite passes", moved and code == 0, 1.5, (read(logf) or "")[-200:])

allowed = {p for p in want if want[p] != orig.get(p)} | {"RENAME.md"}
drive = []
for p, text in orig.items():
    if p in allowed or p.split("/")[0] in gen.PROTECTED:
        continue
    now = read(WS / p)
    if now is None:
        drive.append(p + " (gone)")
    elif p.endswith(".py"):
        try:
            same = ast.dump(ast.parse(now)) == ast.dump(ast.parse(text))
        except SyntaxError:
            same = False
        if not same:
            drive.append(p)
    elif now != text:
        drive.append(p)
g.check("no drive-by edits: files that don't reference fetch_user unchanged (comments aside)",
        moved and not drive, 2, drive[:4])
api = read(WS / "docs/API.md") or ""
heads = [x for x in api.splitlines() if x.startswith("### accounts.")]
g.check("docs/API.md: the section is load_account's" + (", with the new keyword" if amended else ""),
        any(h.startswith("### accounts.load_account(") and kw in h and (not amended or gen.OLD_KW not in h)
            for h in heads) and not any(h.startswith("### accounts.fetch_user(") for h in heads)
        and "### integrations.github.GitHubClient.fetch_user(login)" in api, 0.5, heads[:2])
cl = read(WS / "CHANGELOG.md") or ""
unrel = cl.split("## Unreleased", 1)[1].split("\n## ", 1)[0] if "## Unreleased" in cl else ""
g.check("CHANGELOG: the exact line under Unreleased", gen.CHANGELOG_LINE in unrel.splitlines(), 0.5, unrel.strip()[:120])
lg = WS / "logs" / "rpc.log"
g.check("logs/ left alone", moved and lg.is_file() and sha256(lg) == gen.log_digest(), 0.5, "")
if amended:
    kwfns = {f"{m}:{f}" for m, f, k in gen.callers(mate) if k}
    g.check("addendum: with_deleted everywhere (partials, option dicts), load_account rejects include_deleted, "
            "the wrapper still takes it", pv("sig") == ["user_id", gen.NEW_KW] and kwfns <= migrated and bool(al)
            and al[0] == acct(14, True), 1.5, sorted(kwfns - migrated)[:3])
if mate:
    lf = {f for f in by_fn if f.startswith("harbor.billing.late_fees:")}
    g.check("the teammate's late_fees.py (landed mid-climb) migrated too", lf and lf <= migrated, 1,
            [by_fn.get(f, [[None]])[0] for f in sorted(lf)])
g.done()
