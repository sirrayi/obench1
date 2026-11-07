import os
import random
import subprocess
import sys

BASE = "/private/var/folders/w_/swqg2n117dzdrptxy6074cqw0000gp/T/w/b69927763196"
LOG = "/tmp/verify_status.txt"
log = open(LOG, "w")


def note(msg):
    log.write(str(msg) + "\n")
    log.flush()


try:
    lookup = os.path.join(BASE, "tools", "lookup")
    queries = [l.strip() for l in open(os.path.join(BASE, "queries.txt")) if l.strip()]
    raw = open(os.path.join(BASE, "answers.csv")).read()
    lines = raw.split("\n")
    note("trailing_newline=%s" % (raw.endswith("\n"),))
    if lines and lines[-1] == "":
        lines = lines[:-1]
    note("csv_lines=%d queries=%d" % (len(lines), len(queries)))
    note("header=%r" % lines[0])

    rows = []
    bad = []
    for i, line in enumerate(lines[1:]):
        parts = line.split(",")
        if len(parts) != 2:
            bad.append("shapeline %d %r" % (i + 2, line))
            continue
        part, code = parts
        if part != queries[i]:
            bad.append("order %d %r vs %r" % (i + 2, part, queries[i]))
        if not (code == "NA" or code.isdigit()):
            bad.append("code %d %r" % (i + 2, code))
        rows.append((part, code))
    note("bad=%d" % len(bad))
    for b in bad[:10]:
        note("BAD " + b)

    seen = {}
    dups = 0
    conflicts = 0
    for part, code in rows:
        if part in seen:
            dups += 1
            if seen[part] != code:
                conflicts += 1
                note("DUP_CONFLICT %s %s %s" % (part, seen[part], code))
        else:
            seen[part] = code
    note("unique=%d dup_rows=%d conflicts=%d" % (len(seen), dups, conflicts))

    na_parts = [p for p, c in rows if c == "NA"]
    note("na_rows=%d na_unique=%d" % (len(na_parts), len(set(na_parts))))

    for part in na_parts[:3]:
        r = subprocess.run([sys.executable, lookup, part], capture_output=True, text=True)
        note("na_check %s rc=%d out=%r err=%r" % (part, r.returncode, r.stdout.strip(), r.stderr.strip()[:60]))

    random.seed(7)
    picks = random.sample([p for p, c in rows if c != "NA"], 3)
    for part in picks:
        r = subprocess.run([sys.executable, lookup, part], capture_output=True, text=True)
        note("rand_check %s csv=%s single=%r rc=%d" % (part, seen[part], r.stdout.strip(), r.returncode))

    note("sample_rows=%r" % rows[:2])
    note("last_rows=%r" % rows[-2:])
    note("DONE")
finally:
    log.close()

for p in ("/tmp/run_lookup.py", "/tmp/lookup.terminal"):
    try:
        os.remove(p)
    except OSError:
        pass
