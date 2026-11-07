"""The tally command line."""
import argparse

from tally import __version__, report, store


def main(argv=None):
    """Run one tally command and return its exit status."""
    p = argparse.ArgumentParser(prog="tally")
    p.add_argument("--version", action="version", version="%(prog)s " + __version__)
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
    t = sub.add_parser("top", help="largest expenses")
    t.add_argument("n", type=int)
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
    elif args.cmd == "top":
        for r in report.top(rows, args.n):
            print("%s %.2f %s" % (r["date"], r["amount"], r["category"]))
    return 0
