import gzip
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import WS, write

ck, gw, truth = gen.build()
(WS / "logs").mkdir(parents=True, exist_ok=True)
parts = {"checkout.log.2.gz": [], "checkout.log.1": [], "checkout.log": []}
for t, line in ck:
    parts["checkout.log.2.gz" if t < 8 * 3600 else "checkout.log.1" if t < 16 * 3600 else "checkout.log"].append(line)
for name, lines in parts.items():
    data = ("\n".join(lines) + "\n").encode()
    if name.endswith(".gz"):
        with gzip.GzipFile(WS / "logs" / name, "wb", mtime=0) as f:
            f.write(data)
    else:
        (WS / "logs" / name).write_bytes(data)
(WS / "logs/gateway.log").write_text("\n".join(l for _, l in gw) + "\n")
write("README.md", "# checkout\n\nLogs from 2026-10-29. checkout logs in UTC; the gateway logs in local time (CEST).\n")
save_private("truth.json", truth)
