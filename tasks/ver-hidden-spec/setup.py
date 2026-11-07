import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import commit, git_init, write

write("SPEC.md", gen.SPEC)
write("daterange.py", gen.STUB)
write("tests/__init__.py", "")
write("tests/test_daterange.py", gen.VISIBLE)
git_init()
commit("daterange: spec and stub")
