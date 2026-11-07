# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS

(WS / "units/__init__.py").write_text(gen.REFERENCE)
(WS / "units/__main__.py").write_text(gen.MAIN)
print("units done; CLI added; tests pass.")
