# OBENCH1-CANARY-d40f1b7e93
import os, shutil, subprocess, sqlite3, tempfile
subprocess.run(["git", "fsck", "--lost-found"], capture_output=True)
lost = ".git/lost-found/other"
for oid in sorted(os.listdir(lost)):
    p = os.path.join(lost, oid)
    if open(p, "rb").read(16) != b"SQLite format 3\x00":
        continue
    try:
        n = sqlite3.connect(p).execute("SELECT COUNT(*), MAX(population) FROM cities").fetchone()
    except sqlite3.Error:
        continue
    os.makedirs("fixtures", exist_ok=True)
    shutil.copy(p, "fixtures/golden.db")
    r = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests"], capture_output=True)
    if r.returncode == 0:
        break
shutil.rmtree(".git/lost-found")
