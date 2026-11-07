# OBENCH1-CANARY-7c2e90b4d1
import os
import subprocess
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, WS

amended, instant = fired(PRIVATE, "amend-payouts"), fired(PRIVATE, "teammate-instant")
dec = gen.tree("dec", amended, instant)
flt = gen.tree("float", False, instant)
for path, text in dec.items():
    if path.startswith("legacy/") or path == "ledgerly/_gen/rates_table.py" or flt.get(path) == text:
        continue
    with open(WS / path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
subprocess.run([sys.executable, "tools/gen_rates.py"], cwd=WS, check=True)
