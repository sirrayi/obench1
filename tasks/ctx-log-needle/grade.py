# OBENCH1-CANARY-3be81f02c6
from checks import WS, Grader, load_private, read

g = Grader()
truth = load_private("truth.json")
text = read(WS / "INCIDENT.md") or ""
kv = {}
for line in text.splitlines():
    k, sep, v = line.partition(":")
    if sep:
        kv[k.strip().strip("`*- ").lower()] = v.strip().strip("`* ")
g.check("cause: the key that broke it, not its neighbour", kv.get("cause") == truth["cause"], 1.5, kv.get("cause"))
g.check("applied_at: the reload, in checkout's UTC", kv.get("applied_at") == truth["applied_at"], 1.5, kv.get("applied_at"))
g.check("first_failure: first by time, not by line order", kv.get("first_failure") == truth["first_failure"], 2,
        "picked the line written first" if kv.get("first_failure") == truth["written_first"] else kv.get("first_failure"))
g.check("gateway_502s: only the pool failures, not the inventory timeouts", kv.get("gateway_502s") == str(truth["gateway_502s"]), 2, kv.get("gateway_502s"))
g.check("INCIDENT.md is exactly the four lines", bool(kv) and len([l for l in text.splitlines() if l.strip()]) == 4
        and set(kv) == {"cause", "applied_at", "first_failure", "gateway_502s"}, 0.5, sorted(kv))
g.done()
