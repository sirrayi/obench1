# OBENCH1-CANARY-41b9e6c03a
import json, os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from checks import Grader, WS, read, tree_digest, load_private
import gen
g = Grader()
want = gen.answers()
try:
    got = json.loads(read(WS / "answers.json") or "")
except ValueError:
    got = None
g.check("answers.json parses", isinstance(got, dict), 1)
got = got if isinstance(got, dict) else {}
for k in ("q1", "q2", "q3", "q4", "q5", "q6"):
    v = got.get(k)
    ok = (v == want[k]) if k != "q6" else (isinstance(v, (int, float)) and abs(v - want[k]) < 1e-9)
    g.check(f"{k} correct", ok, 1, f"got {v!r}")
changed = [w["id"] for i, w in enumerate(gen.warehouses())
           if read(WS / f"reports/{w['id'].lower()}.md") != gen.render(w, i)]
g.check("reports left untouched", isinstance(got, dict) and bool(got) and not changed, 1, changed[:5])
g.done()
