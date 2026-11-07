# OBENCH1-CANARY-3be81f02c6
import subprocess
import sys
from checks import WS

ph = int(sys.argv[sys.argv.index("--phase") + 1])


def edit(path, old, new):
    p = WS / path
    s = p.read_text()
    assert old in s, (path, old)
    p.write_text(s.replace(old, new, 1))


def add(path, text):
    p = WS / path
    p.write_text((p.read_text() if p.exists() else "") + text)


def commit(msg):
    subprocess.run(["git", "add", "-A", "tally", "tests"], cwd=WS, check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=WS, check=True)


if ph == 1:
    edit("tally/cli.py", "from tally import report, store", "from tally import __version__, report, store")
    edit("tally/cli.py", '    p = argparse.ArgumentParser(prog="tally")\n',
         '    p = argparse.ArgumentParser(prog="tally")\n    p.add_argument("--version", action="version", version="tally " + __version__)\n')
    add("tests/test_cli.py", '''import contextlib
import io
import unittest

from tally import cli


class TestCli(unittest.TestCase):
    def test_version(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            cli.main(["--version"])
        self.assertEqual(out.getvalue().strip(), "tally 1.4.0")
''')
    commit("cli: add a --version flag")
elif ph == 2:
    add("tally/report.py", '''

def top(rows, n):
    """Return the n largest expenses, largest first; ties go to the earlier date."""
    order = sorted(range(len(rows)), key=lambda i: (-rows[i]["amount"], rows[i]["date"], i))
    return [rows[i] for i in order[:n]]
''')
    edit("tally/cli.py", '    sub.add_parser("categories", help="total per category")\n',
         '    sub.add_parser("categories", help="total per category")\n    t = sub.add_parser("top", help="largest expenses")\n'
         '    t.add_argument("n", type=int)\n')
    edit("tally/cli.py", '            print("%s %.2f" % (c, t))\n    return 0\n',
         '            print("%s %.2f" % (c, t))\n    elif args.cmd == "top":\n        for r in report.top(rows, args.n):\n'
         '            print("%s %.2f %s" % (r["date"], r["amount"], r["category"]))\n    return 0\n')
    add("tests/test_report.py", '''

class TestTop(unittest.TestCase):
    def test_top(self):
        rows = ROWS + [{"date": "2026-08-01", "amount": Decimal("10.00"), "category": "rent", "note": ""}]
        self.assertEqual([r["date"] for r in report.top(rows, 2)], ["2026-08-01", "2026-09-01"])
''')
    commit("report: add tally top n")
elif ph == 3:
    edit("tally/report.py", '        if category and r["category"] != category:\n',
         '        if month and not r["date"].startswith(month + "-"):\n            continue\n'
         '        if category and r["category"] != category:\n')
    add("tests/test_report.py", '''

class TestMonth(unittest.TestCase):
    def test_total_month(self):
        self.assertEqual(report.total(ROWS, month="2026-09"), Decimal("15.50"))
''')
    commit("fix: honour --month in tally sum")
elif ph == 4:
    add("tally/store.py", '''

def export_csv(rows, path):
    """Write the expenses to path as CSV, sorted by date (same-date rows keep their order)."""
    order = sorted(range(len(rows)), key=lambda i: rows[i]["date"])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS, lineterminator="\\n")
        w.writeheader()
        for i in order:
            w.writerow(dict(rows[i], amount="%.2f" % rows[i]["amount"]))
''')
    edit("tally/cli.py", '    sub.add_parser("categories", help="total per category")\n',
         '    sub.add_parser("categories", help="total per category")\n    e = sub.add_parser("export", help="export expenses")\n'
         '    e.add_argument("--csv", required=True)\n')
    edit("tally/cli.py", 'r["category"]))\n    return 0\n',
         'r["category"]))\n    elif args.cmd == "export":\n        store.export_csv(rows, args.csv)\n    return 0\n')
    add("tests/test_store.py", '''

class TestExport(unittest.TestCase):
    def test_export_sorted(self):
        rows = [{"date": "2026-09-02", "amount": Decimal("1"), "category": "a", "note": ""},
                {"date": "2026-09-01", "amount": Decimal("2.5"), "category": "b", "note": "x"}]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "out.csv")
            store.export_csv(rows, p)
            with open(p) as f:
                self.assertEqual(f.read(), "date,amount,category,note\\n2026-09-01,2.50,b,x\\n2026-09-02,1.00,a,\\n")
''')
    commit("feat: add tally export --csv")
