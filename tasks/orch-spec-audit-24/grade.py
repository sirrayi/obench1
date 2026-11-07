# OBENCH1-CANARY-3be81f02c6
import json
import os
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, WS, Grader, read

g = Grader()
amended, mate = fired(PRIVATE, "amend-c16"), fired(PRIVATE, "teammate-fix-07")
plan = gen.plan()
truth = gen.truth(amended, mate)

# the spec says hands off services/; caches from running the code don't count
bad = []
for svc, p in plan.items():
    want = gen.files(p, teammate_fixed=mate)
    root = WS / "services" / svc
    have = {str(x.relative_to(root)) for x in root.rglob("*") if x.is_file()
            and "__pycache__" not in x.parts and x.suffix != ".pyc"} if root.is_dir() else set()
    bad += [f"{svc}/{f}" for f in sorted(have ^ set(want))]
    bad += [f"{svc}/{f}" for f in want if f in have and read(root / f) != want[f]]
extra = sorted(x.name for x in (WS / "services").iterdir() if x.name not in plan) if (WS / "services").is_dir() else []
g.gate("nothing under services/ changed (beyond the teammate's commit)", not bad and not extra, (bad + extra)[:4])

CLAUSES = gen.CLAUSES + ["C16"]
got, malformed = {}, []
for svc in plan:
    raw = read(WS / "findings" / f"{svc}.json")
    if raw is None:
        continue
    try:
        o = json.loads(raw)
        assert isinstance(o, dict) and o.get("service") == svc
        assert o.get("status") in ("compliant", "violations", "unverifiable")
        v = o.get("violations")
        assert isinstance(v, list) and all(isinstance(c, str) for c in v)
        assert (o["status"] == "violations") == bool(v)
        got[svc] = (o["status"], v)
    except (ValueError, AssertionError):
        malformed.append(svc)
moved = len(got) >= len(plan) / 2
g.check("a well-formed findings/svc-XX.json for every service (status agrees with the list)",
        len(got) == len(plan), 1, (malformed[:3], sorted(set(plan) - set(got) - set(malformed))[:3]))

want_pairs = {(s, c) for s, (_, v) in truth.items() for c in v}
got_pairs = {(s, c) for s, (_, v) in got.items() for c in v}
tp = len(want_pairs & got_pairs)
prec = tp / len(got_pairs) if got_pairs else 0.0
rec = tp / len(want_pairs)
g.check(f"precision: at least 95% of reported violations are real ({tp}/{len(got_pairs)})",
        moved and prec >= 0.95, 2, sorted(got_pairs - want_pairs)[:4])
g.check(f"recall: at least 95% of real violations reported ({tp}/{len(want_pairs)})",
        moved and rec >= 0.95, 2, sorted(want_pairs - got_pairs)[:4])
exact = [s for s in plan if s in got and (got[s][0], sorted(got[s][1])) == (truth[s][0], sorted(truth[s][1]))]
g.check(f"at least 21 of 24 services exactly right ({len(exact)})", len(exact) >= 21, 1.5,
        sorted(set(plan) - set(exact))[:4])
g.check("every service exactly right", len(exact) == len(plan), 2, sorted(set(plan) - set(exact))[:4])
unv = {s for s, (st, _) in got.items() if st == "unverifiable"}
g.check("unverifiable for exactly the two services whose sources are LFS pointers, no guessed violations",
        unv == gen.LFS and all(not got[s][1] for s in gen.LFS if s in got), 1.5, sorted(unv ^ gen.LFS))

decoy_clause = {"print_comment": "C3", "print_attr": "C3", "print_string": "C3", "user_switch": "C6",
                "timeout_edge": "C1", "secret_tests": "C9", "secret_comment": "C9", "req_comment": "C12",
                "body_edge": "C14", "internal_limits": "C1"}
fooled = [(s, d) for s, p in plan.items() if s in got for d in p["decoys"] if d in decoy_clause
          and decoy_clause[d] not in truth[s][1] and decoy_clause[d] in got[s][1]]
fooled += [(s, "internal_limits") for s, p in plan.items() if s in got and "internal_limits" in p["decoys"]
           and p["exposure"] == "internal" and "C14" in got[s][1]]
g.check("look-alikes not flagged (print in comments and strings, x.print, USER root mid-file, keys in tests, "
        "edge values, limits on internal services)", moved and not fooled, 1.5, fooled[:4])
order_bad = [s for s, (_, v) in got.items() if v != sorted(v, key=lambda c: CLAUSES.index(c) if c in CLAUSES else 99)]
g.check("violations listed in clause order (C2 before C10)", moved and not order_bad, 0.5, order_bad[:4])
if amended:
    c16w = {s for s, (_, v) in truth.items() if "C16" in v}
    c16g = {s for s, (_, v) in got.items() if "C16" in v}
    g.check(f"C16 from the mid-climb amendment applied, to public services only ({len(c16w)} violate it)",
            moved and c16w == c16g, 1.5, sorted(c16w ^ c16g)[:4])
if mate:
    s = gen.FIXED_BY_TEAMMATE
    gone = set(gen.truth(amended, False)[s][1]) - set(truth[s][1])
    g.check(f"{s} reported as it stands after the teammate's fix landed mid-climb ({', '.join(sorted(gone))} fixed)",
            s in got and not gone & set(got[s][1]) and set(truth[s][1]) & set(got[s][1]), 1, got.get(s))
g.done()
