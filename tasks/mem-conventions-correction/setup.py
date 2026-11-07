import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import PRIVATE
from fixture import commit, git_init, sh, write

for p, t in gen.FILES.items():
    write(p, t)
write("expenses.csv", gen.csv_text(gen.sample("obench1:tally:visible", 40)))
git_init()
for i, msg in enumerate(gen.HISTORY):
    commit(msg)
PRIVATE.mkdir(parents=True, exist_ok=True)
(PRIVATE / "phase-1-start.json").write_text(json.dumps({"head": sh(["git", "rev-parse", "HEAD"]).strip()}))
