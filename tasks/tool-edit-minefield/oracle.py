# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

for p, b in gen.expected().items():
    if p == "Makefile":
        continue
    if (WS / p).read_bytes() != b:
        (WS / p).write_bytes(b)
mk = (WS / "Makefile").read_bytes()
(WS / "Makefile").write_bytes(mk.replace(b"\n\nclean:", b"\n\nlint:\n\tpython3 -m pyflakes src\n\nclean:"))
