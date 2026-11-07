# OBENCH1-CANARY-3be81f02c6
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import WS, Grader, read_bytes, run, tree_digest

g = Grader()
exp = gen.expected()
names = {"config/app.ini": "CRLF ini: [server] timeout only, CRLF kept",
         "src/legacy.py": "latin-1 file: calc renamed, recalc untouched, bytes kept",
         "src/handlers.py": "one of four identical blocks changed",
         "data/catalog.min.json": "1.5 MB one-line JSON: one price, still one line",
         "notes/README.txt": "BOM kept, line added, still no final newline",
         "src/weird name (copy).py": "path with spaces and parentheses"}
moved = False
for p, label in names.items():
    got = read_bytes(WS / p)
    moved = moved or got != gen.FILES[p]
    g.check(label, got == exp[p], 1, "" if got == exp[p] else ("unchanged" if got == gen.FILES[p] else f"{len(got or b'')} bytes"))
mk = read_bytes(WS / "Makefile") or b""
moved = moved or mk != gen.FILES["Makefile"]
code, out = run(["make", "-n", "lint"], timeout=30)
code2, out2 = run(["make", "-n", "test", "clean", "build"], timeout=30)
order = mk.find(b"\ntest:") < mk.find(b"\nlint:") < mk.find(b"\nclean:") if b"\nlint:" in mk else False
rest = mk.replace(b"lint:\n\tpython3 -m pyflakes src\n\n", b"") == gen.FILES["Makefile"]
g.check("Makefile: lint target with a real tab, right after test, nothing else changed",
        code == 0 and out.strip() == "python3 -m pyflakes src" and code2 == 0 and order and rest, 1, out[-120:])
now = tree_digest(WS, exclude=(".git",))
extra = sorted(set(now) - set(gen.FILES))
g.check("no stray files (backups, temp copies)", moved and not extra, 1, extra[:5])
g.done()
