import os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from fixture import write
import gen
write("data/index.bin", gen.encode(gen.table()))
write("queries.txt", "\n".join(gen.queries()) + "\n")
write("tools/lookup", '''#!/usr/bin/env python3
"""Tolerance-code lookup against the parts index.

Usage: lookup <part>

The upstream service is rate-limited, so lookups are serialised through a
lock and paced at one every 1.5 seconds.
"""
import fcntl
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "..", "data", "index.bin")
LOCK = os.path.join(HERE, "..", "data", ".lookup.lock")


def load():
    with open(INDEX, "rb") as f:
        data = f.read()
    assert data[:4] == b"OBIX", "bad index"
    n, key = struct.unpack_from("<IH", data, 4)
    off, table = 10, {}
    for _ in range(n):
        ln = data[off]
        name = bytes(c ^ (key & 0xFF) for c in data[off + 1: off + 1 + ln]).decode()
        (code,) = struct.unpack_from("<H", data, off + 1 + ln)
        table[name] = code ^ key
        off += 3 + ln
    return table


def pace():
    fd = os.open(LOCK, os.O_CREAT | os.O_RDWR)
    fcntl.flock(fd, fcntl.LOCK_EX)
    time.sleep(1.5)
    return fd


def main(argv):
    if len(argv) == 3 and argv[1] == "--batch":
        # Internal: bulk mode for the nightly job. One paced call per file.
        fd = pace()
        table = load()
        for line in open(argv[2]):
            part = line.strip()
            if part:
                print(f"{part}\\t{table.get(part, 'UNKNOWN')}")
        return 0
    if len(argv) != 2 or argv[1].startswith("-"):
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    fd = pace()
    table = load()
    if argv[1] not in table:
        print(f"unknown part: {argv[1]}", file=sys.stderr)
        return 1
    print(table[argv[1]])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
''', mode=0o755)
