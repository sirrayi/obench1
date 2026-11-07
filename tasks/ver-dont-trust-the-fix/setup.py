import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import commit, git_init, sh, write

for p, t in gen.MAIN.items():
    write(p, t)
write("ISSUES/42-export.csv", gen.EXPORT)
git_init()
commit("csv import")
sh(["git", "checkout", "-q", "-b", "fix/42-quoted-newlines"])
write("csvimport/reader.py", gen.FIX)
with open("tests/test_reader.py", "a") as f:
    f.write(gen.FIX_TEST)
commit("Fix #42: keep quoted newlines together (tests pass)", author=("Ali Rahman", "ali@example.com"))
sh(["git", "checkout", "-q", "main"])
refs = sh(["git", "for-each-ref", "--format=%(refname) %(objectname)"])
save_private("start.json", {"refs": refs})
