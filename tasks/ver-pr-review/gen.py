"""ver-pr-review: review a rate-limiter PR. Six real problems of varying
subtlety, three spots that look wrong and aren't. Findings are matched to
bugs by file and line; flagging a decoy costs."""

TASK = ("Review the PR on branch `feature/rate-limit` (against main) as its reviewer. Write REVIEW.md, one finding per "
        "line: `<file>:<line>: <blocker|major|minor>: <what's wrong>`, with the line as it is on the branch. Real "
        "problems only, no style nits. Review only; don't change the branch.")

BASE = {
    "app/__init__.py": "",
    "app/server.py": '''"""HTTP entry point (threaded)."""
from http.server import ThreadingHTTPServer

from app.handlers import Handler


def serve(port=8080):
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
''',
    "app/handlers.py": '''"""Request handlers."""
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
''',
    "tests/__init__.py": "",
}

LIMITER = '''"""Per-client rate limiting: at most `limit` requests per `window` seconds."""
import collections
import threading
import time


class RateLimiter:
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.lock = threading.Lock()
        self.buckets = {}
        # recent rejections, for the /debug page; bounded on purpose
        self.recent = collections.deque(maxlen=50)

    def _bucket(self, key):
        now = time.monotonic()
        b = self.buckets.get(key)
        if b is None or now - b["start"] >= self.window:
            b = {"start": time.time(), "count": 0}  # BUG:clock
            self.buckets[key] = b  # BUG:race
        return b

    def allow(self, key):
        b = self._bucket(key)
        with self.lock:
            b["count"] += 1
            if b["count"] > self.limit + 1:  # BUG:offbyone
                self.recent.append(key)
                return False
            return True

    def retry_after(self, key):
        b = self.buckets.get(key)
        if b is None:
            return 0
        elapsed = time.monotonic() - b["start"]
        return max(0, self.window - elapsed)  # DECOY:clamp

    def whole_seconds(self, seconds):
        # Retry-After takes whole seconds; round down, the client adds jitter (see docs/limits.md)
        return int(seconds) // 1  # DECOY:floor
'''

HANDLERS = '''"""Request handlers."""
from http.server import BaseHTTPRequestHandler

from app.limiter import RateLimiter

LIMITER = RateLimiter(limit=100, window=60)


def client_key(handler):
    # behind the load balancer every request comes from its address, so use the forwarded one
    return handler.headers.get("X-Forwarded-For") or handler.client_address[0]  # BUG:spoof


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        key = client_key(self)
        if not LIMITER.allow(key):
            wait = LIMITER.whole_seconds(LIMITER.retry_after(key))
            self.send_response(429)
            self.send_header("Retry-After", str(wait))
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
'''

TEST = '''import unittest

from app.limiter import RateLimiter


class TestLimiter(unittest.TestCase):
    def test_allows_up_to_the_limit(self):
        rl = RateLimiter(limit=3, window=60)
        for _ in range(3):
            self.assertTrue(rl.allow("a"))  # BUG:weaktest

    def test_separate_clients(self):
        rl = RateLimiter(limit=1, window=60)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("b"))  # DECOY:separate
'''

DOCS = "# Limits\n\nRetry-After is whole seconds, rounded down; clients add 0-1 s of jitter.\nOne bucket per client; idle buckets are dropped after 10 minutes.\n"

BUGS = {
    # tag: (file, severity set accepted, weight, description)
    "offbyone": ("app/limiter.py", {"blocker", "major"}, 1.5, "allows limit+1 requests", r"\+ ?1|off.by.one|one (extra|too many)|limit\s*\+|>=|101"),
    "spoof": ("app/handlers.py", {"blocker", "major"}, 1.5, "client-controlled X-Forwarded-For defeats the limit", r"forward|spoof|forg|client.(controlled|supplied)|header|bypass|rotate"),
    "clock": ("app/limiter.py", {"blocker", "major"}, 1.5, "start stored with time.time but compared with monotonic", r"monotonic|time\.time|clock|wall"),
    "race": ("app/limiter.py", {"major", "blocker"}, 1, "bucket created outside the lock", r"lock|race|thread|concurren|atomic"),
    "weaktest": ("tests/test_limiter.py", {"minor", "major"}, 1, "test never checks the request past the limit", r"limit|reject|past|over|exceed|\+ ?1|never (check|assert)|off.by"),
}
LEAK = ("app/limiter.py", "class RateLimiter", "def _bucket")  # no eviction: buckets grow forever (docs promise 10 min)
DECOYS = ("clamp", "floor", "separate")


def strip(text):
    import re
    return re.sub(r"  # (BUG|DECOY):\w+", "", text)


def lines_of(text):
    """{tag: 1-based line} for the markers in text."""
    import re
    out = {}
    for i, line in enumerate(text.splitlines(), 1):
        m = re.search(r"# (BUG|DECOY):(\w+)", line)
        if m:
            out[m.group(2)] = i
    return out
