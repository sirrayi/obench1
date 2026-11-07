import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import WS, commit, git_init, write

for path, text in gen.tree().items():
    write(path, text)
git_init()
commit("harbor 3.1.0")
(WS / "logs").mkdir(exist_ok=True)
with open(WS / "logs" / "rpc.log", "w", encoding="utf-8") as f:
    gen.rpc_log(f)
