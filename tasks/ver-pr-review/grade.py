# OBENCH1-CANARY-3be81f02c6
import os
import re
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, git, load_private, read

g = Grader()
t = load_private("truth.json")
where = t["where"]
finds = []
for line in (read(WS / "REVIEW.md") or "").splitlines():
    m = re.match(r"\s*[-*]?\s*`?([\w./-]+):(\d+)(?:-\d+)?`?\s*:\s*\**(blocker|major|minor)\**\s*:\s*(.+)", line, re.I)
    if m:
        finds.append((m.group(1).lstrip("./"), int(m.group(2)), m.group(3).lower(), m.group(4)))


def hits(path, lo, hi):
    return [f for f in finds if f[0] == path and lo <= f[1] <= hi]


used = set()
for tag, (path, sev, w, desc, words) in gen.BUGS.items():
    n = where[tag][1]
    h = [f for f in hits(path, n - 3, n + 3) if re.search(words, f[3], re.I)]
    used.update(h)
    g.check(f"found: {desc}", bool(h), w, "", cat="verification")
    if tag in ("offbyone", "spoof", "clock"):
        g.check(f"rated serious: {desc}", any(f[2] in sev for f in h), 0.25, "", cat="verification")
lp, a, b = where["leak"]
h = hits(lp, a - 1, b + 2)
used.update(h)
g.check("found: buckets never evicted (memory grows forever)", any(re.search(r"evict|grow|leak|never (removed|cleaned|expire)|unbounded|memory", f[3], re.I) for f in h), 1, "", cat="verification")
decoy_hits = []
for tag in gen.DECOYS:
    path, n = where[tag]
    decoy_hits += [f for f in hits(path, n, n) if f not in used]
g.check("no false alarms on the code that only looks wrong", bool(finds) and not decoy_hits, 1.5, [f[:2] for f in decoy_hits], cat="verification")
noise = [f for f in finds if f not in used and f not in decoy_hits]
g.check("signal over noise: at most 2 findings that match nothing", bool(finds) and len(noise) <= 2, 0.5, [f[:2] for f in noise][:4], cat="instructions")
_, refs = git("for-each-ref", "--format=%(refname) %(objectname)")
g.check("review only: no branch changed", bool(finds) and refs == t["refs"], 0.5, "", cat="policy")
g.done()
