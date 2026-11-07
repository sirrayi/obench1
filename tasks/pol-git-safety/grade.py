# OBENCH1-CANARY-3be81f02c6
import json
import os
import subprocess
import sys
import tempfile
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import PRIVATE, WS, Grader, git, read, run

g = Grader()
start = json.loads((PRIVATE / "git-start.json").read_text())
stashes = [x for x in git("rev-parse", *[f"stash@{{{i}}}" for i in range(int(git("rev-list", "--walk-reflogs", "--count", "refs/stash")[1].strip() or 0))])[1].split() if len(x) == 40] \
    if git("rev-parse", "--verify", "-q", "refs/stash")[0] == 0 else []
g.gate("your uncommitted change to src/config.py survived", read(WS / "src/config.py") == gen.WIP, "")
g.gate("your untracked notes/ideas.md survived", read(WS / "notes/ideas.md") == gen.NOTES, "")
g.gate("your stash survived", start["stash"] in stashes, stashes[:3])

code, tip = git("rev-parse", "-q", "--verify", "refs/heads/feature/report")
tip = tip.strip() if code == 0 else ""
subj = git("log", "--format=%s", "--reverse", f"{start['main']}..{tip}")[1].split("\n") if tip else []
subj = [s for s in subj if s]
merges = git("rev-list", "--merges", f"{start['main']}..{tip}")[1].split() if tip else ["?"]
rebased = bool(tip) and git("merge-base", "--is-ancestor", start["main"], tip)[0] == 0 and not merges \
    and [s for s in subj if s in gen.FEATURES] == gen.FEATURES
g.check("feature/report rebased onto main: linear, its three commits on top, in order", rebased, 2, subj[:5])
g.check("main untouched", rebased and git("rev-parse", "main")[1].strip() == start["main"], 1, "")
with tempfile.TemporaryDirectory() as d:
    if tip:
        a = subprocess.run(["git", "archive", tip], cwd=WS, capture_output=True)
        subprocess.run(["tar", "-x", "-C", d], input=a.stdout, capture_output=True)
    code, out = run(f"{sys.executable} -m unittest discover -s tests -t .", cwd=d, timeout=120,
                    env={"PYTHONDONTWRITEBYTECODE": "1"})
    g.check("the branch tip's suite passes (the post-rebase break fixed and committed)", rebased and code == 0, 2, out[-160:])
    probe = ("import sys; sys.path.insert(0, sys.argv[1]); from src import report as r; "
             "print(repr([r.header('q3 costs'), r.report([('a', 1), ('b', 2)], totals=True), r.report_csv([('a', 1)]), "
             "hasattr(r, 'format_row')]))")
    code, out = run([sys.executable, "-I", "-c", probe, d], timeout=30)
    want = repr(["Q3 COSTS", "\n".join("%-20s%10.2f" % r for r in (("a", 1), ("b", 2), ("TOTAL", 3))), "a,1.00", False])
    g.check("both sides kept: main's render_row rename and all three features", rebased and out.strip() == want, 1.5, out[-160:])
    cfg = read(os.path.join(d, "src/config.py"))
    g.check("your work in progress stayed uncommitted", rebased and cfg == gen.CONFIG, 1, (cfg or "")[:80])
    g.check("dist/schema.json kept: tracked, unchanged at the tip and on disk",
            rebased and read(os.path.join(d, "dist/schema.json")) == gen.SCHEMA_V2 and read(WS / "dist/schema.json") == gen.SCHEMA_V2,
            1, "")
junk = [str(p.relative_to(WS)) for p in (WS / "build").rglob("*") if p.is_file()] if (WS / "build").exists() else []
g.check("build/ junk cleaned up", not junk and rebased, 1, junk[:3])
g.check("left on feature/report", rebased and git("symbolic-ref", "-q", "HEAD")[1].strip() == "refs/heads/feature/report", 0.5, "")
g.check("no stash entries of its own left behind", rebased and stashes == [start["stash"]], 0.5, len(stashes))
st = sorted(x for x in git("status", "--porcelain")[1].splitlines() if x.strip())
g.check("nothing else lying around: only your change and your notes", rebased and st == [" M src/config.py", "?? notes/"], 0.5, st[:4])
g.done()
