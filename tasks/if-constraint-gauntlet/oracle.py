# OBENCH1-CANARY-4f1c9d2a77
import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

rows = [json.loads(l) for l in (WS / "commits.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
with open(WS / "RELEASE_NOTES.md", "w", encoding="utf-8", newline="") as f:
    f.write(gen.render(rows))
