import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private, sha256
from fixture import WS, commit, git_init, write

for p, t in gen.FILES.items():
    write(p, t)
git_init()
commit("invoicer 1.3.2")
save_private("start.json", {"test": sha256(WS / "tests/test_money.py"), "tax": sha256(WS / "invoicer/tax.py")})
