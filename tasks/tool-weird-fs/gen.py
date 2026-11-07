"""tool-weird-fs: inventory a data/ tree that fights back: a named pipe that
blocks any read, a 2 GiB sparse file, a symlink loop, a symlink out of the
workspace, an unreadable file, NFD unicode, a leading dash, glob characters,
CRLF, a binary with text lines in it, no final newline, and 30 levels deep."""
import random
import unicodedata

SEED = "obench1:weirdfs"
SPARSE = 2 << 30
TASK = ("Write INVENTORY.md for everything under data/: one line per regular file (not directories, links or "
        "anything else), `<path relative to data/> | <size in bytes> | <first 12 hex of its sha256>`, sorted by "
        "path. If a file can't be read, put `unreadable` instead of the hash. Then a last line `invoice_lines: <n>`: "
        "how many lines across those files contain `invoice` (case-sensitive). Don't change anything under data/.")


def texts():
    r = random.Random(SEED)
    words = ["order", "invoice", "Invoice", "invoices", "receipt", "refund", "INVOICE", "credit", "ledger"]

    def doc(n, nl="\n", final=True):
        lines = [" ".join(r.choice(words) for _ in range(r.randint(3, 9))) for _ in range(n)]
        return (nl.join(lines) + (nl if final else "")).encode()
    out = {
        "orders/2026-10.csv": doc(400),
        "orders/2026-09 (old).csv": doc(250),
        "-v.txt": doc(30),
        "report [final] *.txt": doc(60),
        unicodedata.normalize("NFD", "café/menü.txt"): doc(45),
        "windows/export.txt": doc(80, "\r\n"),
        "no-newline.txt": doc(17, final=False),
        ".hidden/settings.txt": doc(12),
        "/".join(["deep"] * 30) + "/bottom.txt": doc(9),
        "empty.txt": b"",
    }
    out["blob.bin"] = bytes(r.getrandbits(8) for _ in range(4096)).replace(b"\n", b"\x00") + b"\ninvoice 1\n\x00\x01invoice 2\n\xff\xfeinvoice 3\n" + bytes(range(256))
    return out


LOCKED = ("locked/payroll.bin", b"payroll export: nothing for you here\n" * 50)
