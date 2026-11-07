# OBENCH1-CANARY-3be81f02c6
"""Before sessions 2-4: note where the previous session left the checkout."""
import json
import os
import subprocess
from checks import PRIVATE, WS

ph = os.environ["OBENCH_PHASE"]
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=WS,
                       capture_output=True, text=True).stdout
(PRIVATE / f"phase-{ph}-start.json").write_text(json.dumps({"head": head, "dirty_before": dirty}))
