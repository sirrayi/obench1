import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import WS, commit, git_init, sh, write

for p, t in gen.FILES.items():
    write(p, t, mode=0o755 if p == "bin/qk" else None)
git_init()
commit("release: 2.2.0")
sh(["git", "tag", "-a", "v2.2.0", "-m", "qk release 2.2.0"])
for i, (msg, path) in enumerate(gen.COMMITS):
    write(path, f"# {msg}\n")
    commit(msg)
head = sh(["git", "rev-parse", "HEAD"]).strip()
log = sh(["git", "log", "--reverse", "--format=%h %s", "v2.2.0..HEAD"]).splitlines()
save_private("start.json", {"head": head, "notes": gen.notes(log)})
