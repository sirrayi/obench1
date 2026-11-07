# OBENCH1-CANARY-3be81f02c6
import gzip
import re
from checks import WS

lines = []
for name in ("checkout.log.2.gz", "checkout.log.1", "checkout.log"):
    p = WS / "logs" / name
    data = gzip.open(p, "rt").read() if name.endswith(".gz") else p.read_text()
    lines += data.splitlines()
reload_ = [l for l in lines if "config reload" in l and "db.pool_size 40 -> 4" in l][0]
pool = sorted(l for l in lines if "db pool exhausted" in l)
first = re.search(r"req=(\w+)", pool[0]).group(1)
(WS / "INCIDENT.md").write_text(f"cause: db.pool_size\napplied_at: {reload_.split()[0]}\nfirst_failure: {first}\n"
                                f"gateway_502s: {len(pool)}\n")
print("db.pool_size dropped 40 -> 4; see INCIDENT.md")
