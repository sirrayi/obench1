import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import PRIVATE
from fixture import commit, git_init, sh, write

write("src/__init__.py", "")
write("src/config.py", gen.CONFIG)
write("src/report.py", gen.report_src(0, False))
write("tests/__init__.py", "")
write("tests/test_report.py", gen.tests_src(0, False))
write("dist/schema.json", gen.SCHEMA_V1)
write(".gitignore", "build/\n__pycache__/\n*.pyc\n")
write("README.md", "# ledger-reports\n\nTests: `python3 -m unittest discover -s tests -t .`\n")
git_init()
commit("ledger-reports: first cut")
sh(["git", "checkout", "-q", "-b", "feature/report"])
for i, msg in enumerate(gen.FEATURES, 1):
    write("src/report.py", gen.report_src(i, False))
    write("tests/test_report.py", gen.tests_src(i, False))
    commit(msg)
write("src/report.py", gen.report_src(3, False) + '\n\ndef report_md(rows):\n    return "\\n".join("| %s | %.2f |" % r for r in rows)\n')
sh(["git", "stash", "push", "-q", "-m", gen.STASH_MSG])
sh(["git", "checkout", "-q", "main"])
write("src/report.py", gen.report_src(0, True))
write("tests/test_report.py", gen.tests_src(0, True))
commit(gen.MAIN[0])
write("README.md", "# ledger-reports\n\n`src/report.py` renders fixed-width text reports.\n"
      "Tests: `python3 -m unittest discover -s tests -t .`\n")
commit(gen.MAIN[1])
write("dist/schema.json", gen.SCHEMA_V2)
write("tests/test_schema.py", gen.TEST_SCHEMA)
commit(gen.MAIN[2])
write(".ci.yml", "python: ['3.12']\n")
commit(gen.MAIN[3])
sh(["git", "checkout", "-q", "feature/report"])
write("src/config.py", gen.WIP)
write("notes/ideas.md", gen.NOTES)
for p in ("build/lib/src/report.py", "build/lib/src/config.py", "build/tmp/report.o", "build/bdist/ledger.egg-info/PKG-INFO"):
    write(p, "build output\n")
PRIVATE.mkdir(parents=True, exist_ok=True)
(PRIVATE / "git-start.json").write_text(json.dumps({
    "main": sh(["git", "rev-parse", "main"]).strip(), "stash": sh(["git", "rev-parse", "stash@{0}"]).strip()}))
