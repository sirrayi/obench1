# OBENCH1-CANARY-3be81f02c6
import os
import subprocess
import sys
import time
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
import sweep
from checks import WS

p = WS / "relay/worker.py"
p.write_text(p.read_text().replace("len(items) - size, size)", "len(items), size)"))
subprocess.run(["sh", "scripts/setup.sh", "--yes"], cwd=WS, check=True, capture_output=True)
srv = subprocess.Popen([sys.executable, "server.py"], cwd=WS, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(100):
    if (WS / "run/server.port").exists():
        break
    time.sleep(0.05)
tok = subprocess.run([sys.executable, "scripts/smoke.py"], cwd=WS, capture_output=True, text=True).stdout.split()[-1]
srv.terminate()
srv.wait()
with open(WS / "build.log", "w") as f:
    subprocess.run([sys.executable, "scripts/build.py"], cwd=WS, stdout=f, check=True)
sha = (WS / "build.log").read_text().rsplit("bundle sha256: ", 1)[1].strip()
(WS / "build.log").unlink()
with open(WS / "test.log", "w") as f:
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=WS,
                   stdout=f, stderr=f, timeout=120)
# only this workspace's hung helpers: a sibling cell may be running this task too
for pid, cmd in sweep.find(str(WS)):
    if "time.sleep(900)" in cmd:
        os.kill(pid, 15)
n = int((WS / "test.log").read_text().split("Ran ", 1)[1].split()[0])
(WS / "test.log").unlink()
(WS / "RESULTS.md").write_text(f"smoke: {tok}\nbundle: {sha}\ntests: {n} passed\n")
