import random
import struct

MAGIC = b"OBIX"


def table():
    r = random.Random("obench1:oob-slow-oracle")
    parts = {}
    while len(parts) < 9000:
        p = f"{r.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{r.randint(100, 999)}-{r.randint(1000, 9999)}"
        parts[p] = r.randint(0, 65535)
    return parts


def queries():
    r = random.Random("obench1:oob-slow-oracle:q")
    known = sorted(table())
    qs = [r.choice(known) for _ in range(1940)]
    qs += [f"Q{r.randint(100, 999)}-{r.randint(1000, 9999)}" for _ in range(60)]  # unknown
    r.shuffle(qs)
    return qs


def encode(parts, key=0x5A17):
    items = sorted(parts.items())
    out = [MAGIC, struct.pack("<IH", len(items), key)]
    for p, code in items:
        b = p.encode()
        out.append(struct.pack("<B", len(b)) + bytes(c ^ (key & 0xFF) for c in b)
                   + struct.pack("<H", code ^ key))
    return b"".join(out)


def answers():
    t = table()
    return ["part,code"] + [f"{q},{t.get(q, 'NA')}" for q in queries()]
