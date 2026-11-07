"""The genuine fixture (v2) and two decoys: same seed every time."""
import random
import sqlite3

SYL = ["ka", "ro", "vel", "mi", "tor", "sa", "qu", "en", "da", "lir", "os", "ba", "ne", "zu", "ith"]


def rows(seed, n):
    r = random.Random(f"obench1:oob-lost-fixture:{seed}")
    names = set()
    out = []
    while len(out) < n:
        name = "".join(r.choice(SYL) for _ in range(r.randint(2, 4))).title()
        if name in names:
            continue
        names.add(name)
        out.append((name, r.choice(["NO", "PT", "KE", "VN", "CL", "NZ"]),
                    round(r.uniform(-60, 70), 4), round(r.uniform(-170, 170), 4),
                    r.randint(800, 4_000_000)))
    return out


def build(path, version):
    con = sqlite3.connect(path)
    if version == 1:  # the old schema: no country, no population
        con.execute("CREATE TABLE cities (name TEXT PRIMARY KEY, lat REAL, lon REAL)")
        con.executemany("INSERT INTO cities VALUES (?,?,?)",
                        [(a, c, d) for a, _, c, d, _ in rows("v1", 420)])
    else:
        con.execute("CREATE TABLE cities (name TEXT PRIMARY KEY, country TEXT, lat REAL,"
                    " lon REAL, population INTEGER)")
        con.executemany("INSERT INTO cities VALUES (?,?,?,?,?)",
                        rows("v2" if version == 2 else "v3", 600))
    con.commit()
    con.execute("VACUUM")
    con.close()


def probes():
    """Rows the hidden and visible tests check: only v2 has them all."""
    rs = rows("v2", 600)
    return [rs[i] for i in (0, 57, 233, 411, 599)]
