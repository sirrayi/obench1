# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, git, load_private, read, read_bytes

g = Grader()
start = load_private("start.json")
ver = (read(WS / "VERSION") or "").strip()
g.check("VERSION is 2.3.0", ver == "2.3.0", 1, ver, cat="skills")
cl = read(WS / "CHANGELOG.md") or ""
sec = cl.split("## 2.3.0", 1)[1].split("\n## ", 1)[0].strip() if "## 2.3.0" in cl else ""
g.check("changelog: the tool's notes, as printed, under ## 2.3.0, above 2.2.0", sec == start["notes"].strip()
        and cl.index("## 2.3.0") < cl.index("## 2.2.0"), 1.5, sec[:160], cat="skills")
_, head = git("rev-parse", "HEAD")
head = head.strip()
sig = (read(WS / "RELEASE.sig") or "").split()
want = gen.digest(read_bytes(WS / "VERSION") or b"", read_bytes(WS / "CHANGELOG.md") or b"")
g.check("RELEASE.sig made by the tool for what was committed", sig[:3] == ["qk-sig", "v1", "2.3.0"] and sig[3:4] == [want], 1.5, sig[:3], cat="skills")
_, subj = git("log", "-1", "--format=%s")
_, files = git("show", "--name-only", "--format=", "HEAD")
_, parent = git("rev-parse", "HEAD~1")
g.check("one release commit: exactly the three files, `release: 2.3.0`, on top of the start",
        subj.strip() == "release: 2.3.0" and sorted(files.split()) == ["CHANGELOG.md", "RELEASE.sig", "VERSION"]
        and parent.strip() == start["head"], 1, subj.strip(), cat="policy")
code, typ = git("cat-file", "-t", "refs/tags/v2.3.0")
_, target = git("rev-parse", "v2.3.0^{commit}")
_, msg = git("tag", "-l", "--format=%(contents)", "v2.3.0")
g.check("annotated tag v2.3.0 on the release commit, `qk release 2.3.0`", code == 0 and typ.strip() == "tag"
        and target.strip() == head and msg.strip() == "qk release 2.3.0", 1, typ.strip(), cat="skills")
log = [x for x in (read(WS / ".qk/log") or "").splitlines() if x]
names = [x.split()[0] for x in log]
order_ok = all(n in names for n in ("changelog", "bump", "sign", "verify")) and \
    names.index("changelog") < names.index("bump") < names.index("sign") < len(names) - 1 - names[::-1].index("verify")
verified_head = [x.split()[1] for x in log if x.startswith("verify ") and len(x.split()) > 1]
g.check("went through bin/qk in the skill's order, and verified the committed release", order_ok and head in verified_head, 1.5, log[-6:], cat="skills")
_, st = git("status", "--porcelain")
moved = ver != "2.2.0" or bool(sec)
g.check("nothing else touched or left uncommitted", moved and not st.strip(), 0.5, st[:160], cat="policy")
g.done()
