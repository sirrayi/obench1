# OBENCH1-CANARY-7c2e90b4d1
"""Runs one package's hidden cases against the workspace: python3 hidden_runner.py cases.json pkg out.json"""
import datetime
import importlib
import inspect
import json
import sys
from decimal import Decimal

cases_path, pkg, out_path = sys.argv[1:4]
sys.path.insert(0, ".")
data = json.load(open(cases_path))
try:
    from ledgerly.money import Money
except Exception as e:  # noqa: BLE001
    json.dump({"fatal": f"{type(e).__name__}: {e}"}, open(out_path, "w"))
    sys.exit(0)


def build(a):
    if isinstance(a, dict):
        k, v = next(iter(a.items()))
        if k == "M":
            return Money(v[0], v[1])
        if k == "D":
            return Decimal(v)
        if k == "L":
            return [build(x) for x in v]
        if k == "T":
            return tuple(build(x) for x in v)
        if k == "date":
            return datetime.date.fromisoformat(v)
    return a


def norm(x):
    if type(x).__name__ == "Money" and isinstance(getattr(x, "amount", None), Decimal):
        v = x.amount
        return ["M", str(v.normalize()) if v else "0", x.currency]
    if isinstance(x, (list, tuple)):
        return [norm(i) for i in x]
    if isinstance(x, float):
        return ["F", repr(x)]
    if isinstance(x, datetime.date):
        return x.isoformat()
    if isinstance(x, (str, bool, int)) or x is None:
        return x
    return repr(x)


results, sigs = [], {}
for c in data["cases"]:
    if c["pkg"] != pkg:
        continue
    try:
        mod = importlib.import_module(c["module"])
        fn = getattr(mod, c["func"])
        key = f"{c['module']}:{c['func']}"
        if key not in sigs:
            try:
                sigs[key] = [[p.name, None if p.default is inspect.Parameter.empty else repr(p.default)
                              .replace("'", '"')] for p in inspect.signature(fn).parameters.values()]
            except (TypeError, ValueError):
                sigs[key] = None
        got = norm(fn(*[build(a) for a in c["args"]]))
        ok = got == c["want"]
        results.append([c["func"], ok, None if ok else str(got)[:120]])
    except Exception as e:  # noqa: BLE001
        results.append([c["func"], False, f"{type(e).__name__}: {e}"[:160]])
json.dump({"results": results, "sigs": sigs}, open(out_path, "w"))
