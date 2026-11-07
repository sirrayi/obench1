import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import WS, commit, git_init, sh, write

for p, t in gen.FILES.items():
    write(p, t)
git_init()
commit("sync: first version")
write(".git/hooks/pre-commit", gen.HOOK, mode=0o755)
save_private("p1.json", {"head": sh(["git", "rev-parse", "HEAD"]).strip()})
