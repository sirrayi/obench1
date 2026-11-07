# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

ENGINE = r'''"""Reads specs/<service>.md (amendments included) and applies it."""
import datetime
import os
import re
from decimal import ROUND_HALF_UP, Decimal

SPECS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specs")
RULE = re.compile(r"^(\d+)\.\s+(\S+)\s+`([^`]+)`(?:\s+(?:->\s+`([^`]+)`|=\s+\"([^\"]*)\"|on\s+\"([^\"]*)\"))?\s*$")


def load(svc):
    text = open(os.path.join(SPECS, svc + ".md"), encoding="utf-8").read()
    head, _, amend = text.partition("\n## Amendment")
    rules = {}
    for line in head.splitlines():
        m = RULE.match(line.strip())
        if m:
            rules[int(m.group(1))] = m.groups()[1:]
    for line in amend.splitlines():
        m = RULE.match(line.strip())
        if m:
            rules[int(m.group(1))] = m.groups()[1:]
    dep = re.search(r"Depends on (\w+):", head)
    return (dep.group(1) if dep else None), [rules[k] for k in sorted(rules)]


def normalize(svc, rec):
    dep, rules = load(svc)
    if dep:
        rec = normalize(dep, rec)
    rec = dict(rec)
    for k, f, to, dflt, sep in rules:
        if k == "require":
            if f not in rec:
                raise ValueError("missing " + f)
            continue
        if k == "default":
            rec.setdefault(f, dflt)
            continue
        if f not in rec:
            continue
        v = rec[f]
        if k in ("strip", "lower", "upper"):
            rec[f] = getattr(v, k)()
        elif k == "rename":
            rec[to] = rec.pop(f)
        elif k == "drop":
            del rec[f]
        elif k == "cents":
            rec[f] = int(Decimal(str(v).strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
        elif k == "bool":
            s = str(v).strip().lower()
            if s not in ("yes", "true", "1", "no", "false", "0"):
                raise ValueError("bad flag")
            rec[f] = s in ("yes", "true", "1")
        elif k == "iso-date":
            rec[f] = datetime.datetime.strptime(v.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
        elif k == "split":
            rec[f] = [p.strip() for p in v.split(sep) if p.strip()]
    return rec
'''
(WS / "clients/_engine.py").write_text(ENGINE)
for svc in gen.SVCS:
    (WS / f"clients/{svc}.py").write_text(f'from clients._engine import normalize as _n\n\n\ndef normalize(record):\n    return _n("{svc}", record)\n')
print("Eight normalizers, one spec-driven engine; amendment 1 to invoices applied.")
