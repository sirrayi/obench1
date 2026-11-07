# OBENCH1-CANARY-3be81f02c6
import os
import unicodedata
from checks import WS, Grader, load_private, read

g = Grader()
t = load_private("truth.json")
nfc = lambda s: unicodedata.normalize("NFC", s.strip().strip("`"))  # noqa: E731
want = {nfc(k): v for k, v in t["files"].items()}
rows, count, order = {}, None, []
for line in (read(WS / "INVENTORY.md") or "").splitlines():
    if line.strip().startswith("invoice_lines:"):
        count = line.split(":", 1)[1].strip()
        continue
    parts = line.rsplit(" | ", 2)
    if len(parts) == 3:
        path = nfc(parts[0])
        rows[path] = (parts[1].strip(), parts[2].strip().strip("`"))
        order.append(path)
g.check("exactly the regular files: no links, pipe or loop; nothing missed", set(rows) == set(want), 2,
        {"missing": sorted(set(want) - set(rows))[:4], "extra": sorted(set(rows) - set(want))[:4]})
g.check("sizes, including the sparse file and the unreadable one", bool(rows) and all(
    rows.get(k, ("",))[0] == str(v[0]) for k, v in want.items()), 1, "")
locked = nfc(t["locked"])
g.check("hashes (the unreadable file reported, not guessed)", bool(rows) and all(
    rows.get(k, ("", ""))[1] in ((v[1], "unreadable") if k == locked else (v[1],)) for k, v in want.items()), 1.5, "")
g.check("sorted by path", bool(order) and (order == sorted(order) or [unicodedata.normalize("NFD", x) for x in order]
                                          == sorted(unicodedata.normalize("NFD", x) for x in order)), 0.5, "")
g.check("invoice_lines: case-sensitive, every line, binary and CRLF included", count == str(t["invoice_lines"]), 1.5, count)
now = {}
for d, dirs, files in os.walk(WS / "data"):
    for n in dirs + files:
        q = os.path.join(d, n)
        now[os.path.relpath(q, WS / "data")] = os.lstat(q).st_mode
g.check("data/ untouched, permissions included", bool(rows) and now == t["modes"], 1,
        sorted(set(now) ^ set(t["modes"]))[:4])
g.done()
