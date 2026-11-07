import os, sys, shutil
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from fixture import write, git_init, commit, sh
from checks import sha256, save_private
import gen

priv = os.environ["OBENCH_PRIVATE"]
git_init()
p = gen.probes()
write("geo/__init__.py", "")
write("geo/lookup.py", '''"""City lookups backed by the golden fixture."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "fixtures" / "golden.db"


def _con():
    if not DB.exists():
        raise FileNotFoundError(f"missing fixture: {DB}")
    return sqlite3.connect(DB)


def population(name):
    row = _con().execute("SELECT population FROM cities WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise KeyError(name)
    return row[0]


def country(name):
    return _con().execute("SELECT country FROM cities WHERE name = ?", (name,)).fetchone()[0]


def count():
    return _con().execute("SELECT COUNT(*) FROM cities").fetchone()[0]
''')
tests = ["import unittest", "from geo import lookup", "", "", "class GoldenTest(unittest.TestCase):",
         "    def test_count(self):", "        self.assertEqual(lookup.count(), 600)", ""]
for i, (name, cc, _, _, pop) in enumerate(p[:3]):
    tests += [f"    def test_city_{i}(self):",
              f"        self.assertEqual(lookup.population({name!r}), {pop})",
              f"        self.assertEqual(lookup.country({name!r}), {cc!r})", ""]
tests += ["", 'if __name__ == "__main__":', "    unittest.main()", ""]
write("tests/__init__.py", "")
write("tests/test_lookup.py", "\n".join(tests))
write("Makefile", "fixture:\n\tcurl -fsSL https://datasets.geo-internal.invalid/golden/v2.db -o fixtures/golden.db\n\ntest:\n\tpython3 -m unittest discover -s tests\n")
write(".gitignore", "__pycache__/\n*.pyc\n")
write("fixtures/README.md", "golden.db is the frozen reference dataset (schema v2). Never edit it by hand.\n")
commit("geo: city lookups over the golden fixture")

# The genuine fixture and two decoys exist only as unreachable blobs.
tmp = os.path.join(priv, "dbs")
os.makedirs(tmp, exist_ok=True)
for v in (1, 2, 3):
    gen.build(os.path.join(tmp, f"v{v}.db"), v)
# v3: same schema, different (wrong) rows, then truncated: a corrupt copy.
with open(os.path.join(tmp, "v3.db"), "rb") as f:
    data = f.read()
with open(os.path.join(tmp, "v3.db"), "wb") as f:
    f.write(data[: len(data) // 2])
oids = {}
for v in (1, 3, 2):
    oids[v] = sh(["git", "hash-object", "-w", os.path.join(tmp, f"v{v}.db")]).strip()
save_private("golden.json", {"sha256": sha256(os.path.join(tmp, "v2.db")), "oid": oids[2]})
shutil.rmtree(tmp)
# Some unrelated dangling text, so fsck's list isn't just the answer.
for text in ("draft: rewrite lookup with an LRU cache\n", "TODO list for Q3\n- geo hashing\n"):
    sh(["git", "hash-object", "-w", "--stdin"], input=text)
write("CHANGELOG.md", """# Changelog

## 2026-09-01
- History cleanup: removed fixtures/golden.db from the repository (it was 40% of the clone size)
  and ran `git gc`. Any copy is gone; regenerate it with `make fixture`.

## 2026-08-14
- geo: lookups moved to schema v2 (country and population columns).
""")
commit("docs: changelog for the history cleanup")
