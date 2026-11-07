# OBENCH1-CANARY-3be81f02c6
import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, run

g = Grader()
PROBE = r'''
import importlib, json, sys
sys.path.insert(0, sys.argv[1])
svc, recs = sys.argv[2], json.loads(sys.stdin.read())
out = []
try:
    fn = importlib.import_module("clients." + svc).normalize
except Exception as e:
    print(json.dumps({"import": repr(e)[:200]})); sys.exit(0)
for r in recs:
    try:
        out.append({"ok": fn(dict(r))})
    except ValueError:
        out.append({"err": "ValueError"})
    except Exception as e:
        out.append({"crash": repr(e)[:80]})
print(json.dumps({"out": out}, ensure_ascii=False))
'''
for svc in gen.SVCS:
    recs = gen.records(svc, 60, "grade")
    want = [gen.outcome(lambda x: gen.normalize(svc, x), r) for r in recs]
    code, out = run([sys.executable, "-I", "-c", PROBE, str(WS), svc], timeout=60, input=json.dumps(recs))
    try:
        got = json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        got = {"import": out[-160:]}
    res = got.get("out") or []
    bad = sum(1 for a, b in zip(res, want) if a != b) + abs(len(res) - len(want))
    dep = f" (on top of {gen.DEPS[svc]})" if svc in gen.DEPS else ""
    cat = "resilience" if svc == gen.AMENDED else None
    g.check(f"{svc}{dep}: all 60 records exactly as the current spec says", not got.get("import") and bad == 0,
            1.5 if svc == gen.AMENDED else 1, got.get("import") or f"{bad} of 60 differ", cat=cat)
g.done()
