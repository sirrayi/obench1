"""A free stand-in for the model provider, for wiring checks only: answers
every chat completion with one short text reply, streamed or not, with usage
that reports a growing cached prefix. Never used in a scored run.

With --probe, a request that offers a shell tool and has no tool result yet
gets one tool call instead: write a file in the workspace, then try to reach
outside the jail (start an app, send an Apple Event, find the computer-use
driver). The tool result that comes back is logged as `probe`, so the wiring
check can see the shell works and the ways out are shut.

    python3 fake_upstream.py --port-file <file> [--log <file>] [--probe]
"""

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

N = {"n": 0}
PROBE = {"on": False}
SHELL_NAMES = ("bash", "shell", "terminal", "run_shell_command", "execute_command", "exec_command", "run_command")
PROBE_CMD = ("echo obench-probe-ok > obench-probe.txt && cat obench-probe.txt; "
             "perl -e 'alarm 10; exec(@ARGV) or exit 99' open -g -j -a 'System Events' >/dev/null 2>&1; echo open=$?; "
             "perl -e 'alarm 10; exec(@ARGV) or exit 99' osascript -e 'tell application \"Terminal\" to get count of windows' "
             ">/dev/null 2>&1; echo osa=$?; command -v cua-driver >/dev/null; echo cua=$?")


def shell_call(body):
    """(tool name, arguments) for the request's shell tool, or None."""
    for t in body.get("tools") or []:
        f = t.get("function") or t
        if f.get("name") not in SHELL_NAMES:
            continue
        props = (f.get("parameters") or {}).get("properties") or {}
        key = next((k for k in ("command", "cmd", "script") if k in props), None)
        if key:  # any other required text field (dsh's bash wants a description) gets a plain label
            args = {k: "obench wiring probe" for k in (f.get("parameters") or {}).get("required") or []
                    if (props.get(k) or {}).get("type") == "string"}
            return f["name"], {**args, key: PROBE_CMD}
    return None


def tool_result(body):
    for m in reversed(body.get("messages") or []):
        if m.get("role") == "tool":
            c = m.get("content")
            return c if isinstance(c, str) else json.dumps(c)
    return None
LOCK = threading.Lock()
LOG = {}


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def do_GET(self):
        out = json.dumps({"object": "list", "data": [{"id": "deepseek-v4.1-flash", "object": "model"}]}).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(out)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("content-length") or 0)) or b"{}")
        with LOCK:
            N["n"] += 1
            n = N["n"]
        result = tool_result(body)
        call = shell_call(body) if PROBE["on"] and result is None else None
        if LOG.get("path"):
            with LOCK, open(LOG["path"], "a") as f:
                f.write(json.dumps({"n": n, "path": self.path, "ua": self.headers.get("user-agent"),
                                    "session": self.headers.get("x-opencode-session"),
                                    "model": body.get("model"), "stream": body.get("stream"),
                                    "reasoning": {k: body[k] for k in ("reasoning_effort", "thinking", "reasoning",
                                                                       "enable_thinking") if k in body},
                                    "params": {k: body[k] for k in ("max_tokens", "max_completion_tokens", "temperature",
                                                                    "top_p", "tool_choice", "parallel_tool_calls")
                                               if k in body},
                                    "tools": len(body.get("tools") or []),
                                    "probe_call": call[0] if call else None,
                                    "probe": result[:2000] if PROBE["on"] and result is not None else None}) + "\n")
        usage = {"prompt_tokens": 1000 * n, "completion_tokens": 5,
                 "prompt_tokens_details": {"cached_tokens": 1000 * (n - 1)}}
        text = "Done.\nEND OF REPORT"
        if call:
            tc = {"index": 0, "id": f"call_probe_{n}", "type": "function",
                  "function": {"name": call[0], "arguments": json.dumps(call[1])}}
            if body.get("stream"):
                self.send_response(200)
                self.send_header("content-type", "text/event-stream")
                self.end_headers()
                chunks = [{"choices": [{"index": 0, "delta": {"role": "assistant", "tool_calls": [tc]}}]},
                          {"choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}]},
                          {"choices": [], "usage": usage}]
                for c in chunks:
                    c.update(id=f"fake-{n}", object="chat.completion.chunk", model=body.get("model"))
                    self.wfile.write(b"data: " + json.dumps(c).encode() + b"\n\n")
                self.wfile.write(b"data: [DONE]\n\n")
                return
            tc.pop("index")
            out = json.dumps({"id": f"fake-{n}", "object": "chat.completion", "model": body.get("model"),
                              "choices": [{"index": 0, "finish_reason": "tool_calls",
                                           "message": {"role": "assistant", "content": None, "tool_calls": [tc]}}],
                              "usage": usage}).encode()
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(out)
            return
        if body.get("stream"):
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            chunks = [{"choices": [{"index": 0, "delta": {"role": "assistant", "content": text}}]},
                      {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
                      {"choices": [], "usage": usage}]
            for c in chunks:
                c.update(id=f"fake-{n}", object="chat.completion.chunk", model=body.get("model"))
                self.wfile.write(b"data: " + json.dumps(c).encode() + b"\n\n")
            self.wfile.write(b"data: [DONE]\n\n")
            return
        out = json.dumps({"id": f"fake-{n}", "object": "chat.completion", "model": body.get("model"),
                          "choices": [{"index": 0, "finish_reason": "stop",
                                       "message": {"role": "assistant", "content": text}}],
                          "usage": usage}).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port-file", required=True)
    ap.add_argument("--log")
    ap.add_argument("--probe", action="store_true")
    a = ap.parse_args()
    LOG["path"] = a.log
    PROBE["on"] = a.probe
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    open(a.port_file, "w").write(str(srv.server_address[1]))
    srv.serve_forever()


if __name__ == "__main__":
    main()
