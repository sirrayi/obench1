"""ctx-log-needle: a day of checkout and gateway logs (~65 MB, rotated, one
file gzipped; gateway in local time, checkout in UTC; workers interleave so
line order isn't time order). Find the config change that caused the 502s,
when it landed, the first request it broke, and how many 502s it caused
(not counting the unrelated inventory timeouts that also show up as 502s)."""
import gzip
import random
from datetime import datetime, timedelta, timezone

SEED = "obench1:needle"
DAY = datetime(2026, 10, 29, tzinfo=timezone.utc)
LOCAL = timezone(timedelta(hours=2))
RELOADS = [(3 * 3600 + 12 * 60 + 5.001, "log.level info -> debug"),
           (6 * 3600 + 58 * 60 + 41.337, "cache.ttl_s 300 -> 600, db.pool_size 40 -> 4"),
           (14 * 3600 + 20 * 60 + 5.120, "db.pool_size 4 -> 40")]
BAD_FROM, BAD_TO = 7 * 3600 + 31 * 60 + 10, 14 * 3600 + 20 * 60 + 5
PATHS = [("GET", "/cart"), ("GET", "/cart/summary"), ("POST", "/cart/items"), ("POST", "/cart/checkout")]
TASK = ("Checkout started throwing 502s yesterday morning, after someone touched its config. The logs are in logs/ "
        "(the gateway's and checkout's, rotated). Work out which config key did it, when that change was applied, "
        "the first customer request that failed because of it, and how many 502s the gateway served because of it. "
        "Write INCIDENT.md with exactly four lines: `cause: <config key>`, `applied_at: <UTC timestamp as checkout "
        "logged it>`, `first_failure: <request id>`, `gateway_502s: <count>`.")


def iso(t):
    d = DAY + timedelta(seconds=t)
    return d.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % int(round((t % 1) * 1000) % 1000)


def gw_ts(t):
    return (DAY + timedelta(seconds=int(t))).astimezone(LOCAL).strftime("%d/%b/%Y:%H:%M:%S +0200")


def build():
    """(checkout lines by UTC hour, gateway lines, truth)."""
    r = random.Random(SEED)
    ck = []  # (t, line)
    gw = []
    truth = {"cause": "db.pool_size", "applied_at": iso(RELOADS[1][0]), "gateway_502s": 0}
    for t, change in RELOADS:
        ck.append((t, f"{iso(t)} INFO main config reload from /etc/checkout/checkout.yaml: {change}"))

    def req(t, worker, fail=None):
        rid = "%012x" % r.getrandbits(48)
        meth, path = PATHS[r.randrange(4)] if fail is None else ("POST", "/cart/checkout")
        if fail == "pool":
            ck.append((t, f"{iso(t)} ERROR w{worker} req={rid} {meth} {path} -> 500 db pool exhausted (size=4, waiting={r.randint(5, 30)})"))
        elif fail == "inv":
            ck.append((t, f"{iso(t)} ERROR w{worker} req={rid} {meth} {path} -> 500 inventory call timed out after 3000ms"))
        else:
            ck.append((t, f"{iso(t)} INFO w{worker} req={rid} {meth} {path} -> 200 {r.randint(8, 220)}ms"))
        gw.append((t, f'{gw_ts(t)} "{meth} {path}" {502 if fail else 200} req={rid} upstream=checkout {r.randint(9, 240)}ms'))
        return rid

    for s in range(86400):
        hour = s / 3600
        rate = 2 + (4 if 7 <= hour < 21 else 0)
        for _ in range(r.randint(rate - 1, rate + 1)):
            t = s + r.random() * 0.999
            w = r.randint(1, 4)
            if s == BAD_FROM:
                continue
            fail = None
            if BAD_FROM < s < BAD_TO and r.random() < 0.025:
                fail = "pool"
            elif r.random() < 0.0015:
                fail = "inv"
            req(t, w, fail)
            if BAD_FROM - 1500 < s < BAD_TO and r.random() < 0.004:
                ck.append((t + 0.0004, f"{iso(t + 0.0004)} WARN w{w} db pool near capacity (4/4 in use)"))
        if s == BAD_FROM:
            # two workers log out of order: the later failure is written first
            late = req(s + 0.412, 3, "pool")
            truth["first_failure"] = req(s + 0.409, 1, "pool")
            truth["written_first"] = late
    # workers flush in batches: line order is roughly, not strictly, time order
    ck.sort(key=lambda x: x[0])
    for i in range(0, len(ck) - 1, 7):
        if ck[i][1][24:29] != "ERROR" and ck[i + 1][1][24:29] != "ERROR" and r.random() < 0.3:
            ck[i], ck[i + 1] = ck[i + 1], ck[i]
    ff = truth["first_failure"]
    j = next(i for i, (_, l) in enumerate(ck) if f"req={ff}" in l)
    k = next(i for i, (_, l) in enumerate(ck) if f"req={truth['written_first']}" in l)
    if k > j:
        ck[j], ck[k] = ck[k], ck[j]
    truth["gateway_502s"] = sum(1 for _, l in ck if "db pool exhausted" in l)
    gw.sort(key=lambda x: x[0])
    return ck, gw, truth
