"""The model gateway every OBench1 harness talks through (127.0.0.1 only).

One proxy for every harness, so tokens, cache hits, latency and provider
faults mean the same thing whichever harness is climbing:

- meter: each POST is one call; its usage is read from the upstream
  response (JSON or SSE; OpenAI chat, DeepSeek, Anthropic and Responses
  shapes) and logged as {n, prompt, cached, output, ttfb_s, wall_s}.
  `prompt` always includes cached tokens.
- faults, by call index (1-based): a fixed `schedule`, `bursts` (every
  call in [from, to] faults, kinds cycled — a storm the harness must ride
  out), then a seeded background `rate` up to `max`.

  429      429 + Retry-After: 3, never forwarded
  500/503  server_error / overloaded, never forwarded
  error200 200 whose JSON body is an error object, never forwarded
  stall    hold STALL seconds, then forward
  trickle  forward, but drip the body (0.4 s between 256-byte pieces)
  cut      forward, then drop the connection mid-body
  garbage  forward, with a malformed SSE line first

Model calls go upstream with one set of model settings for every harness
(--model-params): the same model, thinking on, the same reasoning effort
and the same output ceiling, whatever the harness asked for; the call's log
line keeps what it asked for. Everything else in a request goes upstream
unchanged (headers included); the gateway never sees or adds credentials
beyond what the harness sends. One header is copied,
not invented: dsh names its session x-deepseek-harness-session-id, and
the same id also rides as x-opencode-session, the name OpenCode Go keys
its cache routing on (pi and omp send that header themselves).

    python3 gateway.py --upstream https://opencode.ai/zen/go/v1 --plan '{...}' \
        --log <file> --port-file <file>
"""

import argparse
import http.client
import json
import os
import random
import socket
import socketserver
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

KINDS = ["429", "500", "503", "error200", "stall", "cut", "garbage", "trickle"]
STATE = {"n": 0, "faults": 0}
LOCK = threading.Lock()
CFG = {}


def log(**kw):
    kw["t"] = round(time.time(), 3)
    with LOCK, open(CFG["log"], "a") as f:
        f.write(json.dumps(kw) + "\n")


def live_bursts():
    """Bursts an avalanche switched on mid-run (the control file), re-read
    whenever it changes."""
    path = CFG.get("control")
    if not path:
        return []
    try:
        mtime = os.stat(path).st_mtime_ns
    except OSError:
        return []
    if STATE.get("ctl_mtime") != mtime:
        try:
            STATE["ctl"] = json.loads(open(path).read()).get("bursts") or []
            STATE["ctl_mtime"] = mtime
        except (OSError, ValueError):
            pass
    return STATE.get("ctl") or []


MODEL_PATHS = ("/chat/completions", "/completions", "/messages", "/responses")


def model_call(method, path):
    """A model call: what the meter counts and the fault plan numbers. Anything
    else (a model-info probe, say) passes through unnumbered, so it can't shift
    a harness's fault schedule."""
    return method == "POST" and path.split("?", 1)[0].rstrip("/").endswith(MODEL_PATHS)


def same_model(body):
    """Every harness's model call leaves with the same model, thinking on, the
    same reasoning effort and the same output ceiling (the field the harness
    used, else max_tokens). Returns the new body and what the harness asked
    for where it differed."""
    want = CFG.get("model_params")
    if not want or not body:
        return body, None
    try:
        obj = json.loads(body)
    except ValueError:
        return body, None
    if not isinstance(obj, dict):
        return body, None
    asked = {}
    out_field = "max_completion_tokens" if "max_completion_tokens" in obj else "max_tokens"
    for k, v in (("model", want["model"]), ("thinking", {"type": "enabled"}),
                 ("reasoning_effort", want["reasoning_effort"]), (out_field, want["max_output"])):
        if obj.get(k) != v:
            asked[k] = obj.get(k)
            obj[k] = v
    for k in ("reasoning", "enable_thinking"):  # other spellings of the same knob
        if k in obj:
            asked[k] = obj.pop(k)
    return (json.dumps(obj).encode() if asked else body), (asked or None)


def next_fault(method, path):
    with LOCK:
        if not model_call(method, path):
            return 0, None
        STATE["n"] += 1
        n = STATE["n"]
        plan = CFG["plan"]
        fault = (plan.get("schedule") or {}).get(str(n))
        for b in (plan.get("bursts") or []) + live_bursts():
            if fault is None and b["from"] <= n <= b["to"]:
                kinds = b.get("kinds") or ["429"]
                fault = kinds[(n - b["from"]) % len(kinds)]
        if fault is None and STATE["faults"] < plan.get("max", 0):
            rng = random.Random(plan.get("seed", 0) * 100003 + n)
            if rng.random() < plan.get("rate", 0.0):
                fault = rng.choice(plan.get("kinds", KINDS))
        if fault:
            STATE["faults"] += 1
        return n, fault


def usage_of(u):
    """(prompt incl. cached, cached, output) from one usage object."""
    if not isinstance(u, dict):
        return None
    if "cache_read_input_tokens" in u or "cache_creation_input_tokens" in u:  # Anthropic
        cached = u.get("cache_read_input_tokens") or 0
        prompt = (u.get("input_tokens") or 0) + cached + (u.get("cache_creation_input_tokens") or 0)
        return prompt, cached, u.get("output_tokens") or 0
    if "prompt_tokens" in u:  # chat completions (OpenAI, DeepSeek, most compat servers)
        details = u.get("prompt_tokens_details") or {}
        cached = details.get("cached_tokens") or u.get("prompt_cache_hit_tokens") or 0
        return u.get("prompt_tokens") or 0, cached, u.get("completion_tokens") or 0
    if "input_tokens" in u:  # Responses API, or Anthropic without cache fields
        details = u.get("input_tokens_details") or {}
        return u.get("input_tokens") or 0, details.get("cached_tokens") or 0, u.get("output_tokens") or 0
    return None


class Meter:
    """Usage from a response body as it streams past, without holding it."""

    def __init__(self, sse):
        self.sse, self.buf, self.body, self.found = sse, b"", b"", {}

    def _take(self, obj):
        for u in (obj.get("usage"), (obj.get("message") or {}).get("usage"),
                  (obj.get("response") or {}).get("usage")):
            got = usage_of(u)
            if got:
                prompt, cached, out = got
                # Anthropic splits usage across message_start and message_delta
                self.found["prompt"] = max(prompt, self.found.get("prompt", 0))
                self.found["cached"] = max(cached, self.found.get("cached", 0))
                self.found["output"] = max(out, self.found.get("output", 0))

    def feed(self, chunk):
        if not self.sse:
            if len(self.body) < 8 << 20:
                self.body += chunk
            return
        self.buf += chunk
        while b"\n\n" in self.buf.replace(b"\r\n", b"\n"):
            norm = self.buf.replace(b"\r\n", b"\n")
            event, _, rest = norm.partition(b"\n\n")
            self.buf = rest
            for line in event.split(b"\n"):
                if line.startswith(b"data:"):
                    try:
                        obj = json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if isinstance(obj, dict):
                        self._take(obj)

    def result(self):
        if not self.sse and self.body:
            try:
                obj = json.loads(self.body)
                if isinstance(obj, dict):
                    self._take(obj)
            except ValueError:
                pass
        return self.found or None


class Proxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # the response ends at close: no length games

    def _reply(self, status, obj, extra=None):
        out = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(out)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(out)

    def _forward(self, method):
        n, fault = next_fault(method, self.path)
        t0 = time.time()
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length) if length else None
        if n:
            body, asked = same_model(body)
            log(n=n, ev="call", path=self.path, fault=fault, bytes_in=length, **({"asked": asked} if asked else {}))
        elif method == "POST":
            log(ev="other", path=self.path, bytes_in=length)
        canned = {"429": (429, "rate limited", "rate_limit_error", {"retry-after": "3"}),
                  "500": (500, "internal error", "server_error", None),
                  "503": (503, "overloaded", "overloaded_error", None),
                  "error200": (200, "upstream failed", "server_error", None)}
        if fault in canned:
            status, msg, typ, extra = canned[fault]
            err = {"message": f"{msg} (obench gateway)", "type": typ}
            if fault == "error200":
                err["code"] = 500
            return self._reply(status, {"error": err}, extra)
        if fault == "stall":
            time.sleep(CFG["stall"])
        up = urlsplit(CFG["upstream"])
        rest = self.path[len("/v1"):] if self.path.startswith("/v1") else self.path
        path = up.path.rstrip("/") + rest
        Conn = http.client.HTTPSConnection if up.scheme == "https" else http.client.HTTPConnection
        conn = Conn(up.netloc, timeout=900)
        skip = {"host", "content-length", "accept-encoding", "connection"}
        headers = {k: v for k, v in self.headers.items() if k.lower() not in skip}
        sid = self.headers.get("x-deepseek-harness-session-id")
        if sid and "x-opencode-session" not in {k.lower() for k in headers}:
            headers["x-opencode-session"] = sid
        try:
            conn.request(method, path, body=body, headers=headers)
            r = conn.getresponse()
        except OSError as e:
            log(n=n, ev="upstream_error", error=str(e)[:200])
            return self._reply(502, {"error": {"message": f"gateway upstream error: {e}"}})
        ttfb = time.time() - t0
        self.send_response(r.status)
        for k, v in r.getheaders():
            if k.lower() not in {"transfer-encoding", "content-length", "connection", "content-encoding"}:
                self.send_header(k, v)
        self.end_headers()
        meter = Meter("event-stream" in (r.getheader("content-type") or ""))
        if fault == "garbage":
            self.wfile.write(b"data: {not json, obench gateway\n\n")
        sent, cut_at, how = 0, CFG["cut_at"], "ok"
        try:
            while True:
                chunk = r.read1(8192)
                if not chunk:
                    break
                meter.feed(chunk)
                if fault == "cut" and (sent + len(chunk) >= cut_at or sent == 0):
                    # mid-body: past cut_at, or halfway into a short first chunk
                    keep = cut_at - sent if sent + len(chunk) >= cut_at and sent else len(chunk) // 2
                    self.wfile.write(chunk[: max(0, min(keep, len(chunk) - 1))])
                    self.wfile.flush()
                    self.connection.shutdown(socket.SHUT_RDWR)
                    how = "cut"
                    break
                if fault == "trickle":
                    for i in range(0, len(chunk), 256):
                        self.wfile.write(chunk[i:i + 256])
                        self.wfile.flush()
                        time.sleep(0.4)
                else:
                    self.wfile.write(chunk)
                    self.wfile.flush()
                sent += len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            how = "client_gone"
        finally:
            conn.close()
        if method == "POST":
            u = meter.result() or {}
            log(n=n, ev="done", status=r.status, how=how, bytes_out=sent, ttfb_s=round(ttfb, 3),
                wall_s=round(time.time() - t0, 3), **u)

    def do_POST(self):
        self._forward("POST")

    def do_GET(self):
        self._forward("GET")

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--plan", default="{}")
    ap.add_argument("--log", required=True)
    ap.add_argument("--port-file", required=True)
    ap.add_argument("--stall", type=float, default=40.0)
    ap.add_argument("--cut-at", type=int, default=600)
    ap.add_argument("--control", help="JSON file of live bursts an avalanche may write mid-run")
    ap.add_argument("--model-params", default="",
                    help='JSON {"model", "reasoning_effort", "max_output"} every model call is sent with')
    a = ap.parse_args()
    CFG.update(upstream=a.upstream, plan=json.loads(a.plan), log=a.log, stall=a.stall, cut_at=a.cut_at,
               control=a.control, model_params=json.loads(a.model_params) if a.model_params else None)
    open(a.log, "a").close()
    socketserver.TCPServer.allow_reuse_address = True
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
    with open(a.port_file, "w") as f:
        f.write(str(srv.server_address[1]))
    srv.serve_forever()


if __name__ == "__main__":
    main()
