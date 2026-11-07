# OBENCH1-CANARY-3be81f02c6
import hashlib
import os
import stat
from checks import WS

data = WS / "data"
rows, lines = [], 0
for d, dirs, files in os.walk(data):
    for n in files:
        p = os.path.join(d, n)
        st = os.lstat(p)
        if not stat.S_ISREG(st.st_mode):
            continue
        rel = os.path.relpath(p, data)
        try:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(8 << 20), b""):
                    h.update(chunk)
            digest = h.hexdigest()[:12]
            if st.st_size < (1 << 30):
                with open(p, "rb") as f:
                    lines += sum(1 for line in f.read().split(b"\n") if b"invoice" in line)
        except PermissionError:
            digest = "unreadable"
        rows.append(f"{rel} | {st.st_size} | {digest}")
(WS / "INVENTORY.md").write_text("\n".join(sorted(rows)) + f"\ninvoice_lines: {lines}\n")
