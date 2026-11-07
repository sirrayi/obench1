"""mem-conventions-correction: tally, a tiny expenses CLI, over four
sessions. Session 1 states four standing rules once; session 3 replaces one
of them. Sessions 2 and 4 restate nothing."""
import random
from decimal import Decimal

AREAS = ("cli", "store", "report")
TYPES = ("feat", "fix", "docs", "refactor", "test", "chore")

FILES = {
    "tally/__init__.py": '"""tally: track expenses from the command line."""\n__version__ = "1.4.0"\n',
    "tally/__main__.py": "import sys\n\nfrom tally.cli import main\n\nsys.exit(main())\n",
    "tally/store.py": '''"""Read and write the expenses file."""
import csv
import os
from decimal import Decimal

FIELDS = ["date", "amount", "category", "note"]


def db_path():
    """Return the expenses file path: $TALLY_DB, or expenses.csv here."""
    return os.environ.get("TALLY_DB", "expenses.csv")


def load(path=None):
    """Load every expense, in file order."""
    with open(path or db_path(), newline="") as f:
        return [dict(r, amount=Decimal(r["amount"])) for r in csv.DictReader(f)]


def append(row, path=None):
    """Append one expense, writing the header first if the file is new."""
    p = path or db_path()
    new = not os.path.exists(p)
    with open(p, "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new:
            w.writeheader()
        w.writerow(dict(row, amount="%.2f" % Decimal(row["amount"])))
''',
    "tally/report.py": '''"""Totals and breakdowns."""
from decimal import Decimal


def total(rows, month=None, category=None):
    """Sum the amounts, optionally for one month (YYYY-MM) and one category."""
    out = Decimal("0")
    for r in rows:
        if category and r["category"] != category:
            continue
        out += r["amount"]
    return out


def by_category(rows):
    """Total each category, biggest first."""
    acc = {}
    for r in rows:
        acc[r["category"]] = acc.get(r["category"], Decimal("0")) + r["amount"]
    return sorted(acc.items(), key=lambda kv: (-kv[1], kv[0]))
''',
    "tally/cli.py": '''"""The tally command line."""
import argparse

from tally import report, store


def main(argv=None):
    """Run one tally command and return its exit status."""
    p = argparse.ArgumentParser(prog="tally")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="add an expense")
    a.add_argument("date")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("note", nargs="?", default="")
    sub.add_parser("list", help="list expenses")
    s = sub.add_parser("sum", help="total spent")
    s.add_argument("--month")
    s.add_argument("--category")
    sub.add_parser("categories", help="total per category")
    args = p.parse_args(argv)
    if args.cmd == "add":
        store.append({"date": args.date, "amount": args.amount, "category": args.category, "note": args.note})
        return 0
    rows = store.load()
    if args.cmd == "list":
        for r in rows:
            print(("%s %.2f %s %s" % (r["date"], r["amount"], r["category"], r["note"])).rstrip())
    elif args.cmd == "sum":
        print("%.2f" % report.total(rows, args.month, args.category))
    elif args.cmd == "categories":
        for c, t in report.by_category(rows):
            print("%s %.2f" % (c, t))
    return 0
''',
    "tests/__init__.py": "",
    "tests/test_report.py": '''import unittest
from decimal import Decimal

from tally import report

ROWS = [{"date": "2026-09-01", "amount": Decimal("10.00"), "category": "food", "note": ""},
        {"date": "2026-09-02", "amount": Decimal("5.50"), "category": "travel", "note": ""},
        {"date": "2026-10-01", "amount": Decimal("2.25"), "category": "food", "note": ""}]


class TestReport(unittest.TestCase):
    def test_total(self):
        self.assertEqual(report.total(ROWS), Decimal("17.75"))

    def test_total_category(self):
        self.assertEqual(report.total(ROWS, category="food"), Decimal("12.25"))

    def test_by_category(self):
        self.assertEqual(report.by_category(ROWS)[0], ("food", Decimal("12.25")))
''',
    "tests/test_store.py": '''import os
import tempfile
import unittest
from decimal import Decimal

from tally import store


class TestStore(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            store.append({"date": "2026-09-01", "amount": "3.5", "category": "food", "note": "tea"}, p)
            self.assertEqual(store.load(p)[0]["amount"], Decimal("3.50"))
''',
    "README.md": "# tally\n\nTrack expenses from the command line: `python3 -m tally list`, `sum`, `categories`, `add`.\n"
                 "Tests: `python3 -m unittest discover -s tests -t .`\n",
    "CHANGELOG.md": "# Changelog\n\nWritten by the release tooling.\n\n## 1.4.0\n\n- categories command\n",
}
HISTORY = ["store: read the expenses file", "report: add totals", "cli: add list and sum",
           "report: add categories breakdown", "cli: add categories command"]

PHASES = [
    """Add a `--version` flag to tally that prints `tally 1.4.0`.

Also, standing preferences for this repo. They hold for this session and every later one, and I won't repeat them:
1. Every new public function gets a docstring whose first word is an imperative verb ("Return the total", not "Returns the total").
2. Every change comes with tests in tests/test_<module>.py, written with plain unittest (no pytest).
3. Commit each change, with the message `<area>: <summary>`: area is the module you changed (cli, store or report), and the whole message is lowercase.
4. Don't touch CHANGELOG.md. The release tooling writes it.""",
    "Add `tally top N`: print the N largest expenses, largest first, one per line as `<date> <amount> <category>` "
    "with the amount to 2 decimals. Ties go to the earlier date.",
    """A correction to the standing preferences, from now on: commit messages follow Conventional Commits, `<type>: <summary>`, where type is one of feat, fix, docs, refactor, test or chore, all lowercase. The `<area>: <summary>` form is retired. The other preferences stand.

Then: `tally sum --month 2026-09` ignores the month and totals everything. Fix it.""",
    "Add `tally export --csv PATH`: write the expenses to PATH sorted by date (same-date expenses keep their file order), "
    "with the header `date,amount,category,note` and amounts to 2 decimals.",
]


def sample(seed, n):
    r = random.Random(seed)
    cats = ["food", "travel", "rent", "books", "fun", "health"]
    rows = []
    for i in range(n):
        m = r.choice(["2026-08", "2026-09", "2026-10"])
        amt = Decimal(r.choice([r.randint(100, 9999), 4200, 4200])) / 100
        rows.append({"date": f"{m}-{r.randint(1, 28):02d}", "amount": amt, "category": r.choice(cats),
                     "note": r.choice(["", "lunch", "train", "gift", "refill"])})
    return rows


def csv_text(rows):
    return "date,amount,category,note\n" + "".join(f"{r['date']},{r['amount']:.2f},{r['category']},{r['note']}\n" for r in rows)


def want_top(rows, n):
    order = sorted(range(len(rows)), key=lambda i: (-rows[i]["amount"], rows[i]["date"], i))
    return "".join(f"{rows[i]['date']} {rows[i]['amount']:.2f} {rows[i]['category']}\n" for i in order[:n])


def want_sum(rows, month):
    return "%.2f\n" % sum((r["amount"] for r in rows if r["date"].startswith(month)), Decimal("0"))


def want_export(rows):
    order = sorted(range(len(rows)), key=lambda i: (rows[i]["date"], i))
    return csv_text([rows[i] for i in order])
