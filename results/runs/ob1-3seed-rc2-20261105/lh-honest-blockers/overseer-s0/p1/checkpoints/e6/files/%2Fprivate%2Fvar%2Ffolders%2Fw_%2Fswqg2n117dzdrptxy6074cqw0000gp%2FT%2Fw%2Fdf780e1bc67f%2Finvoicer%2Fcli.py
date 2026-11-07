"""Print an invoice's total."""
import argparse
import json

from invoicer.money import total


def main(argv=None):
    ap = argparse.ArgumentParser(prog="invoicer")
    ap.add_argument("invoice")
    a = ap.parse_args(argv)
    with open(a.invoice) as f:
        inv = json.load(f)
    print(f"{inv['client']}: {total(inv['lines'])}")


if __name__ == "__main__":
    main()
