import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import commit, git_init, write

tks, cat, buggy, twin = gen.plan()
write("fleetd/__init__.py", '"""fleetd: the fleet control plane."""\n__version__ = "2.8.0"\n')
for mod in gen.MODULES:
    write(f"fleetd/{mod}.py", gen.module_src(mod, "buggy"))
write("fleetd/wiring.py", '"""Wires the policy helpers into the service graph."""\nfrom fleetd import '
      + ", ".join(gen.MODULES) + "  # noqa: F401\n")
write("pyproject.toml", '[project]\nname = "fleetd"\nversion = "2.8.0"\nrequires-python = ">=3.9"\n')
write("CONTRIBUTING.md", gen.CONTRIBUTING)
write("CHANGELOG.md", "# Changelog\n\n## Unreleased\n\n## 2.8.0\n\n- Storage v2 workers.\n- Quiet hours per region.\n")
write("README.md", "# fleetd\n\nThe fleet control plane. Open tickets are in TICKETS/.\n")
for t in tks[:18]:
    write(f"TICKETS/TCK-{t['n']}.md", gen.ticket_md(t))
write("tests/__init__.py", "")
write("tests/test_tickets.py", "import unittest\n\n\nclass TestTickets(unittest.TestCase):\n    pass\n")
smoke = [f for f in cat if f["name"] not in buggy][::400][:6]
lines = ["import unittest", ""] + [f"from fleetd.{f['module']} import {f['name']}" for f in smoke] + \
        ["", "", "class TestSmoke(unittest.TestCase):"]
for f in smoke:
    args = gen.probes(f["kind"], f["c"])[0]
    res = gen.run_one(gen.compiled(f), args)
    if res[0] == "ok":
        lines += [f"    def test_{f['name']}(self):", f"        self.assertEqual({f['name']}(*{args!r}), {res[1]!r})", ""]
write("tests/test_smoke.py", "\n".join(lines) + "\n")
git_init()
commit("fleetd 2.8.0")
