"""tool-edit-minefield: seven small edits, each in a file built to trip an
edit tool: CRLF endings, a Makefile's tabs, latin-1 bytes, four identical
blocks, a 1.5 MB one-line JSON, a BOM with no final newline, and a path with
spaces and parentheses. Every byte outside the edit must survive."""
import json
import random

SEED = "obench1:minefield"
TASK = """Make these seven edits, and change nothing else in any file:

1. `config/app.ini`: in the `[server]` section, set `timeout` to 45.
2. `Makefile`: add a `lint` target right after `test`, whose recipe runs `python3 -m pyflakes src`.
3. `src/legacy.py`: rename the function `calc` to `calculate` and update its callers.
4. `src/handlers.py`: in `delete_account` only, a missing user should raise `PermissionError("no user")` instead of returning None.
5. `data/catalog.min.json`: the price of SKU `K-7731` is now 17.49.
6. `notes/README.txt`: add the line `Reviewed: 2026-10-30` at the end (the file has no trailing newline; keep it that way).
7. `src/weird name (copy).py`: turn DEBUG off.
"""


def catalog():
    r = random.Random(SEED)
    items = []
    for i in range(16000):
        sku = "K-%d" % (1000 + i * 7 % 90000)
        items.append({"sku": sku, "price": round(r.uniform(1, 300), 2), "name": "Item %05d" % i,
                      "tags": r.sample(["red", "blue", "kit", "spare", "bulk", "eco"], 2), "related": []})
    items[300]["sku"] = "K-77310"
    items[301]["sku"] = "K-7731"
    items[301]["price"] = 19.99
    items[9000]["related"] = ["K-7731"]
    items[9001]["price"] = 19.99
    return json.dumps({"version": 3, "items": items}, separators=(",", ":"))


def handler(name):
    return f'''def {name}(db, user_id):
    user = db.get(user_id)
    if not user:
        return None
    return db.{name.split("_")[0]}(user)


'''


FILES = {
    "config/app.ini": ("[client]\r\ntimeout = 30\r\nretries = 3\r\n\r\n[server]\r\nhost = 0.0.0.0\r\ntimeout = 30\r\n"
                       "workers = 4\r\n\r\n[cache]\r\ntimeout = 30\r\n").encode(),
    "Makefile": b".PHONY: test clean build\n\nbuild:\n\tpython3 -m build\n\ntest:\n\tpython3 -m unittest discover -s tests\n\n"
                b"clean:\n\trm -rf build dist\n",
    "src/handlers.py": ('"""Account handlers."""\n\n\n' + "".join(handler(n) for n in ("get_account", "update_account", "delete_account", "export_account"))).encode(),
    "notes/README.txt": "﻿Release notes\n=============\n\nNothing yet.".encode("utf-8"),
    "src/weird name (copy).py": b"# copy of settings for the staging box\nDEBUG = True\nDEBUG_SQL = True\nNAME = 'staging'\n",
    "src/__init__.py": b"",
}
FILES["src/legacy.py"] = ("# -*- coding: latin-1 -*-\n# Autor: José Nuñez, Zürich\n\n\ndef calc(a, b):\n"
                          "    return a * b + 1\n\n\ndef recalc(xs):\n    return [calc(x, 2) for x in xs]\n\n\n"
                          "def report(xs):\n    total = sum(calc(x, 3) for x in xs)\n    return \"Gesamt: %d\" % total\n").encode("latin-1")
FILES["data/catalog.min.json"] = catalog().encode()


def expected():
    e = dict(FILES)
    e["config/app.ini"] = FILES["config/app.ini"].replace(b"host = 0.0.0.0\r\ntimeout = 30\r\n", b"host = 0.0.0.0\r\ntimeout = 45\r\n")
    e["src/legacy.py"] = FILES["src/legacy.py"].replace(b"def calc(", b"def calculate(").replace(b"[calc(", b"[calculate(").replace(b"sum(calc(", b"sum(calculate(")
    h = FILES["src/handlers.py"].decode()
    a, b = h.split("def delete_account", 1)
    b = b.replace("        return None\n", '        raise PermissionError("no user")\n', 1)
    e["src/handlers.py"] = (a + "def delete_account" + b).encode()
    e["data/catalog.min.json"] = FILES["data/catalog.min.json"].replace(b'"sku":"K-7731","price":19.99', b'"sku":"K-7731","price":17.49')
    e["notes/README.txt"] = FILES["notes/README.txt"] + b"\nReviewed: 2026-10-30"
    e["src/weird name (copy).py"] = FILES["src/weird name (copy).py"].replace(b"DEBUG = True\n", b"DEBUG = False\n")
    return e
