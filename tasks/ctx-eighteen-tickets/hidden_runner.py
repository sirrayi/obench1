# OBENCH1-CANARY-3be81f02c6
"""python3 hidden_runner.py cases.json out.json — runs fleetd functions on hidden inputs."""
import importlib
import json
import sys

sys.path.insert(0, ".")
cases = json.load(open(sys.argv[1]))
out = []
for c in cases:
    try:
        fn = getattr(importlib.import_module(f"fleetd.{c['module']}"), c["func"])
        try:
            got = ["ok", fn(*c["args"])]
        except Exception as e:  # noqa: BLE001
            got = ["raise", type(e).__name__]
        got = json.loads(json.dumps(got, default=repr))
        out.append([c["id"], got == c["want"], None if got == c["want"] else str(got)[:100]])
    except Exception as e:  # noqa: BLE001
        out.append([c["id"], False, f"{type(e).__name__}: {e}"[:120]])
json.dump(out, open(sys.argv[2], "w"))
