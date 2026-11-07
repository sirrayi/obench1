"""lh-hang-gauntlet: a project whose every step can hang a harness: a setup
script that asks on stdin, a server that has to run in the background, a
build that prints 30 MB before its one useful line, and a test suite that
leaks a grandchild holding the output pipe open. And: leave nothing running."""
import hashlib

SEED = "obench1:hang"

FILES = {
    "README.md": """# relay

1. `scripts/setup.sh` initialises the local database (it asks first; `--help` says how not to be asked).
2. `python3 server.py` serves the API on a free port and writes the port to run/server.port.
3. `python3 scripts/smoke.py` checks a running server and prints its smoke token.
4. `python3 scripts/build.py` builds build/relay.bundle and prints its checksum at the very end.
5. Tests: `python3 -m unittest discover -s tests -t .`
""",
    "scripts/setup.sh": """#!/bin/sh
# Initialise the local database.
if [ "$1" = "--help" ]; then
  echo "usage: setup.sh [--yes]   (--yes: don't ask, just initialise)"; exit 0
fi
if [ "$1" != "--yes" ]; then
  printf "This will create data/relay.db. Proceed? [y/N] "
  read -r answer
  [ "$answer" = "y" ] || { echo "aborted"; exit 1; }
fi
mkdir -p data
python3 -c 'import json; json.dump({"relays": 12, "region": "eu-west"}, open("data/relay.db", "w"))'
echo "database ready"
""",
    "server.py": '''"""The relay API (development server)."""
import hashlib
import http.server
import json
import os


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/smoke":
            self.send_error(404)
            return
        try:
            db = open("data/relay.db").read()
        except OSError:
            self.send_error(500, "no database: run scripts/setup.sh first")
            return
        token = hashlib.sha256(("relay:" + db).encode()).hexdigest()[:16]
        body = json.dumps({"ok": True, "token": token}).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    os.makedirs("run", exist_ok=True)
    with open("run/server.port", "w") as f:
        f.write(str(srv.server_address[1]))
    srv.serve_forever()
''',
    "scripts/smoke.py": '''"""Check a running relay server: prints its smoke token."""
import json
import sys
import urllib.request

try:
    port = open("run/server.port").read().strip()
except OSError:
    sys.exit("no run/server.port: is the server running?")
print("smoke token:", json.load(urllib.request.urlopen("http://127.0.0.1:%s/smoke" % port, timeout=10))["token"])
''',
    "scripts/build.py": '''"""Build build/relay.bundle. Verbose: it logs every module it packs."""
import hashlib
import os
import random

r = random.Random(7)
os.makedirs("build", exist_ok=True)
h = hashlib.sha256()
with open("build/relay.bundle", "wb") as out:
    for i in range(400000):
        chunk = ("relay-module-%06d:%08x\\n" % (i, r.getrandbits(32))).encode()
        out.write(chunk)
        h.update(chunk)
        print("packing module %06d of 400000 ... ok (%d bytes, cache warm, no warnings)" % (i, len(chunk)))
print("bundle sha256:", h.hexdigest())
''',
    "relay/__init__.py": "",
    "relay/worker.py": '''"""Split work into batches for the relay workers."""


def chunks(items, size):
    """Split items into lists of at most size items, in order."""
    return [items[i:i + size] for i in range(0, len(items) - size, size)]
''',
    "tests/__init__.py": "",
    "tests/test_worker.py": '''import subprocess
import sys
import unittest

from relay.worker import chunks


class TestWorker(unittest.TestCase):
    def test_chunks(self):
        self.assertEqual(chunks([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_warm_cache(self):
        # warms the shared cache for the other tests (a helper that lingers)
        subprocess.Popen([sys.executable, "-c", "import time; time.sleep(900)"])
        self.assertTrue(True)
''',
    ".gitignore": "build/\nrun/\ndata/\n__pycache__/\n",
}
TASK = ("Get relay checked end to end: set up the database, start the server, run the smoke check and the build, "
        "run the tests and fix whatever fails. Then write RESULTS.md with exactly three lines: `smoke: <token>`, "
        "`bundle: <sha256>` and `tests: <n> passed`. Leave nothing running when you're done.")


def bundle_sha():
    import random
    r = random.Random(7)
    h = hashlib.sha256()
    for i in range(400000):
        h.update(("relay-module-%06d:%08x\n" % (i, r.getrandbits(32))).encode())
    return h.hexdigest()


def smoke_token():
    import json
    db = json.dumps({"relays": 12, "region": "eu-west"})
    return hashlib.sha256(("relay:" + db).encode()).hexdigest()[:16]
