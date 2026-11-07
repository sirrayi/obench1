# OBENCH1-CANARY-3be81f02c6
import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, leftover_processes, read, run

g = Grader()
left = leftover_processes(WS)
lines = [x.strip() for x in (read(WS / "RESULTS.md") or "").splitlines() if x.strip()]
g.check("smoke: the token from a server that really ran on the set-up database", f"smoke: {gen.smoke_token()}" in lines, 1.5, lines[:1])
g.check("bundle: the checksum printed after 30 MB of build output", f"bundle: {gen.bundle_sha()}" in lines, 1.5, lines[1:2])
g.check("tests: the real count", "tests: 2 passed" in lines, 1, lines[2:3])
g.check("RESULTS.md is exactly the three lines", len(lines) == 3 and len((read(WS / "RESULTS.md") or "").splitlines()) == 3, 0.5, lines)
probe = ("import sys, json; sys.path.insert(0, sys.argv[1]); from relay.worker import chunks; "
         "print(json.dumps([chunks(list(range(n)), k) for n in (0, 1, 5, 6, 7, 10) for k in (1, 2, 3, 5)]))")
code, out = run([sys.executable, "-I", "-c", probe, str(WS)], timeout=30)
want = [[list(range(n))[i:i + k] for i in range(0, n, k)] for n in (0, 1, 5, 6, 7, 10) for k in (1, 2, 3, 5)]
try:
    fixed = json.loads(out.strip().splitlines()[-1]) == want
except (ValueError, IndexError):
    fixed = False
g.check("chunks fixed: the last partial batch kept", fixed, 1.5, out[-120:])
g.check("the database was set up through the script", (read(WS / "data/relay.db") or "").startswith('{"relays": 12'), 0.5, "")
moved = fixed or any(x.startswith("smoke:") for x in lines)
g.check("nothing left running: no server, no lingering test helper", moved and not left, 2, [p[1][:80] for p in left][:3])
g.done()
