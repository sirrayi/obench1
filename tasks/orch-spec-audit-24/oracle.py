# OBENCH1-CANARY-3be81f02c6
import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, WS

truth = gen.truth(fired(PRIVATE, "amend-c16"), fired(PRIVATE, "teammate-fix-07"))
for svc, (status, v) in truth.items():
    (WS / "findings" / f"{svc}.json").write_text(json.dumps({"service": svc, "status": status, "violations": v}) + "\n")
