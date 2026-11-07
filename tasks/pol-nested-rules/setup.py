import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import commit, git_init, write

for p, t in gen.FILES.items():
    write(p, t)
write(".gitignore", "__pycache__/\n")
git_init()
commit("atlas: edge and web")
