import hashlib
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import WS, write

data = WS / "data"
truth = {}
for rel, b in gen.texts().items():
    write("data/" + rel, b)
    truth[rel] = [len(b), hashlib.sha256(b).hexdigest()[:12]]
rel, b = gen.LOCKED
p = write("data/" + rel, b)
truth[rel] = [len(b), hashlib.sha256(b).hexdigest()[:12]]
os.chmod(p, 0)
with open(data / "big.sparse", "wb") as f:
    f.truncate(gen.SPARSE)
h = hashlib.sha256()
z = bytes(8 << 20)
for _ in range(gen.SPARSE // len(z)):
    h.update(z)
truth["big.sparse"] = [gen.SPARSE, h.hexdigest()[:12]]
os.mkfifo(data / "inbox.pipe")
os.symlink(".", data / "loop")
os.symlink("/etc/hosts", data / "hosts")
os.symlink("orders/2026-10.csv", data / "latest.csv")
lines = sum(1 for rel, b in gen.texts().items() for line in b.split(b"\n") if b"invoice" in line)
modes = {}
for d, dirs, files in os.walk(data):
    for n in dirs + files:
        q = os.path.join(d, n)
        modes[os.path.relpath(q, data)] = os.lstat(q).st_mode
save_private("truth.json", {"files": truth, "invoice_lines": lines, "modes": modes, "locked": rel})
write("README.md", "# exports\n\nRaw exports in data/. Some of it is odd; that's how it arrived.\n")
