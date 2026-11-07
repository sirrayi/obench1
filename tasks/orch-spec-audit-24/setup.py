import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import commit, git_init, write

write("SPEC.md", gen.SPEC)
write("README.md", "# platform-services\n\nTwenty-four services, one baseline spec (SPEC.md).\n"
      "Audit reports go in findings/.\n")
for svc, p in gen.plan().items():
    for rel, text in gen.files(p).items():
        write(f"services/{svc}/{rel}", text)
write("findings/.gitkeep", "")
git_init()
commit("platform services, spec rev 7")
