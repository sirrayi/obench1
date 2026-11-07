"""Fault-injecting proxy for OpenAI-compatible providers (roadmap ch. 15/22.1).

The harness talks to http://127.0.0.1:<port>/v1; requests go upstream
unchanged except where the fault plan says otherwise. Faults, by request
index (1-based):

  429      429 + Retry-After: 3, never forwarded
  500      500 server_error, never forwarded
  503      503 overloaded, never forwarded
  error200 200 whose JSON body is an error object, never forwarded
  stall    hold the request STALL seconds, then forward normally
  cut      forward, then drop the connection mid-body (no [DONE])
  garbage  forward, with a malformed SSE line written first

After the fixed schedule, each request faults with probability RATE
(seeded), up to MAX faults in all. Every request is logged as one JSON line.

    python3 chaos_proxy.py --upstream https://opencode.ai/zen/go/v1 \
        --plan '{"schedule": {"1": "429"}, "rate": 0.15, "seed": 7, "max": 14}' \
        --log <file> --port-file <file>
"""

import argparse
import http.client
import json
import random
import socket
import socketserver
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

KINDS = ["429", "500", "503", "error200", "stall", "cut", "garbage"]
STATE = {"n": 0, "faults": 0}
LOCK = threading.Lock()
CFG = {}


def log(**kw):
    kw["t"] = round(time.time(), 3)
    with LOCK, open(CFG["log"], "a") as f:
        f.write(json.dumps(kw) + "\n")


def next_fault():
    with LOCK:
        STATE["n"] += 1
        n = STATE["n"]
        plan = CFG["plan"]
        fault = plan.get("schedule", {}).get(str(n))
        if fault is None and STATE["faults"] < plan.get("max", 0):
            rng = random.Random(plan.get("seed", 0) * 100003 + n)
            if rng.random() < plan.get("rate", 0.0):
                fault = rng.choice(plan.get("kinds", KINDS))
        if fault:
            STATE["faults"] += 1
        return n, fault


class Proxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # response ends at close: no length games

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
        n, fault = next_fault()
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length) if length else None
        log(n=n, method=method, path=self.path, fault=fault, bytes_in=length)
        if fault == "429":
            return self._reply(429, {"error": {"message": "rate limited (obench chaos)",
                                               "type": "rate_limit_error"}}, {"retry-after": "3"})
        if fault == "500":
            return self._reply(500, {"error": {"message": "internal error (obench chaos)",
                                               "type": "server_error"}})
        if fault == "503":
            return self._reply(503, {"error": {"message": "overloaded (obench chaos)",
                                               "type": "overloaded_error"}})
        if fault == "error200":
            return self._reply(200, {"error": {"message": "upstream failed (obench chaos)",
                                               "type": "server_error", "code": 500}})
        if fault == "stall":
            time.sleep(CFG["stall"])
        up = urlsplit(CFG["upstream"])
        rest = self.path[len("/v1"):] if self.path.startswith("/v1") else self.path
        path = up.path.rstrip("/") + rest
        Conn = http.client.HTTPSConnection if up.scheme == "https" else http.client.HTTPConnection
        conn = Conn(up.netloc, timeout=600)
        skip = {"host", "content-length", "accept-encoding", "connection"}
        headers = {k: v for k, v in self.headers.items() if k.lower() not in skip}
        try:
            conn.request(method, path, body=body, headers=headers)
            r = conn.getresponse()
        except OSError as e:
            log(n=n, upstream_error=str(e))
            return self._reply(502, {"error": {"message": f"proxy upstream error: {e}"}})
        self.send_response(r.status)
        for k, v in r.getheaders():
            if k.lower() not in {"transfer-encoding", "content-length", "connection",
                                 "content-encoding"}:
                self.send_header(k, v)
        self.end_headers()
        if fault == "garbage":
            self.wfile.write(b"data: {not json, obench chaos\n\n")
        sent = 0
        cut_at = CFG["cut_at"]
        try:
            while True:
                chunk = r.read1(8192)
                if not chunk:
                    break
                if fault == "cut" and sent + len(chunk) >= cut_at:
                    self.wfile.write(chunk[: max(0, cut_at - sent)])
                    self.wfile.flush()
                    self.connection.shutdown(socket.SHUT_RDWR)
                    log(n=n, cut_after=cut_at)
                    return
                self.wfile.write(chunk)
                self.wfile.flush()
                sent += len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            log(n=n, client_gone=True)
        finally:
            conn.close()
        log(n=n, status=r.status, bytes_out=sent)

    def do_POST(self):
        self._forward("POST")

    def do_GET(self):
        self._forward("GET")

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--port-file", required=True)
    ap.add_argument("--stall", type=float, default=40.0)
    ap.add_argument("--cut-at", type=int, default=600)
    a = ap.parse_args()
    CFG.update(upstream=a.upstream, plan=json.loads(a.plan), log=a.log, stall=a.stall,
               cut_at=a.cut_at)
    open(a.log, "a").close()
    socketserver.TCPServer.allow_reuse_address = True
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
    with open(a.port_file, "w") as f:
        f.write(str(srv.server_address[1]))
    srv.serve_forever()


if __name__ == "__main__":
    main()
