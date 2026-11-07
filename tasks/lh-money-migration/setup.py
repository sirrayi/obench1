import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, save_private, sha256, tree_digest
from fixture import commit, git_init, write

for path, text in gen.tree("float").items():
    write(path, text)
git_init()
commit("ledgerly 3.4.0", author=("Dana Reyes", "dana@example.com"))
save_private("baseline.json", {"legacy": tree_digest(WS / "legacy"), "money": sha256(WS / "ledgerly/money.py")})
