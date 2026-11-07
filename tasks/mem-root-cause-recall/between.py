# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

_, good = gen.feed("apac", "v2", "2026-10", "obench1:meridian:apac:2026-10")
(WS / "ISSUE-2.md").write_text(gen.ISSUE_2.format(good=f"{good:,.2f}", bad=f"{good * 100:.2f}"))
