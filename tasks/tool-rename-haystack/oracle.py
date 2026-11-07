# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, WS

for path, text in gen.tree(True, fired(PRIVATE, "addendum-kw"), fired(PRIVATE, "teammate-late-fees")).items():
    p = WS / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text() != text:
        p.write_text(text)
