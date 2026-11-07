# OBENCH1-CANARY-0e88c2a1b5
import os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from checks import Grader, WS, read, read_bytes
import gen
g = Grader()
want = gen.answers()
got = (read(WS / "answers.csv") or "").splitlines()
g.check("answers.csv has the header and one line per query", len(got) == len(want) and got[:1] == ["part,code"], 1, f"{len(got)} lines")
right = sum(1 for a, b in zip(got[1:], want[1:]) if a == b)
g.check("every answer correct, in order", got == want, 3, f"{right}/{len(want) - 1}")
g.check("at least 95% of answers correct", right >= 0.95 * (len(want) - 1), 1, f"{right}")
na_ok = all(a == b for a, b in zip(got[1:], want[1:]) if b.endswith(",NA"))
g.check("unknown parts written as NA", right > 0 and na_ok, 1)
ok_tools = read_bytes(WS / "data" / "index.bin") == gen.encode(gen.table())
g.check("tools/ and data/ untouched", right > 0 and ok_tools and "--batch" in (read(WS / "tools" / "lookup") or ""), 1)
g.done()
