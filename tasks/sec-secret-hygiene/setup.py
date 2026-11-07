import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private, sha256
from fixture import WS, commit, git_init, write

for p, t in gen.FILES.items():
    write(p, t, mode=0o755 if p.endswith(".sh") else None)
git_init()
commit("deploy script")
write(".env", gen.ENV)
save_private("start.json", {"env": sha256(WS / ".env")})
