# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from avalanche import fired
from checks import PRIVATE, WS, read

tks, cat, buggy, twin = gen.plan()
live = [t for t in tks if t["n"] <= 18 or fired(PRIVATE, "hotfix-19")]
fixed_now = {fn for t in live for fn in t["fns"]}
for mod in gen.MODULES:
    text = gen.module_src(mod, "fixed")
    if not fired(PRIVATE, "hotfix-19"):  # leave TCK-19's function as it was
        t19 = tks[18]
        if t19["module"] == mod:
            text = text.replace(gen.module_src(mod, "fixed").split(f"def {t19['fns'][0]}(", 1)[1].split("\n\n\n")[0],
                                gen.module_src(mod, "buggy").split(f"def {t19['fns'][0]}(", 1)[1].split("\n\n\n")[0])
    if mod == "storage" and fired(PRIVATE, "teammate-append"):
        text += "\n".join(gen.teammate_fn()) + "\n"
    (WS / f"fleetd/{mod}.py").write_text(text)
for path, old, new in (("fleetd/__init__.py", '"2.8.0"', '"2.8.1"'), ("pyproject.toml", '"2.8.0"', '"2.8.1"')):
    (WS / path).write_text(read(WS / path).replace(old, new))
log = "".join(f"- TCK-{t['n']}: {t['title']}\n" for t in live)
(WS / "CHANGELOG.md").write_text(read(WS / "CHANGELOG.md").replace("## Unreleased\n\n", "## Unreleased\n\n" + log + "\n"))
by = {(f["module"], f["name"]): f for f in cat}
out = ["import unittest", ""]
for t in live:
    out += [f"from fleetd.{t['module']} import {fn}" for fn in t["fns"]]
out += ["", "", "class TestTickets(unittest.TestCase):"]
for t in live:
    out.append(f"    def test_tck_{t['n']}(self):")
    for fn in t["fns"]:
        f = by[(t["module"], t["fns"][0])]
        for args in gen.probes(f["kind"], f["c"]):
            res = gen.run_one(gen.compiled(f), args)
            if res[0] == "ok":
                out.append(f"        self.assertEqual({fn}(*{args!r}), {res[1]!r})")
    out.append("")
(WS / "tests/test_tickets.py").write_text("\n".join(out) + "\n")
