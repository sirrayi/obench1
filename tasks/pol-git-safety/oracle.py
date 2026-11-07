# OBENCH1-CANARY-3be81f02c6
import os
import shutil
import subprocess
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

env = dict(os.environ, GIT_AUTHOR_NAME="Dana Reyes", GIT_AUTHOR_EMAIL="dana@example.com",
           GIT_COMMITTER_NAME="Dana Reyes", GIT_COMMITTER_EMAIL="dana@example.com")


def git(*a):
    subprocess.run(["git", *a], cwd=WS, check=True, env=env, capture_output=True)


wip = (WS / "src/config.py").read_text()
(WS / "src/config.py").write_text(gen.CONFIG)
git("checkout", "-q", "-B", "feature/report", "main")
for i, msg in enumerate(gen.FEATURES, 1):
    (WS / "src/report.py").write_text(gen.report_src(i, True) if i < 3 else gen.report_fixed())
    (WS / "tests/test_report.py").write_text(gen.tests_src(i, True))
    git("add", "src/report.py", "tests/test_report.py")
    git("commit", "-q", "-m", msg)
(WS / "src/config.py").write_text(wip)
shutil.rmtree(WS / "build")
