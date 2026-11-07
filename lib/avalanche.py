"""Avalanches: what the mountain throws at a harness mid-climb.

A task lists them in task.json under "avalanches":

  {"id": "amend-1", "phase": 1, "after_calls": 8, "after_s": 300, "action": "drop",
   "src": "avalanche/AMENDMENT-1.md", "dst": "AMENDMENTS/001.md"}
  {"id": "teammate", "after_calls": 40, "after_s": 1500, "action": "commit",
   "files": {"ledgerly/payouts/instant.py": "avalanche/instant.py"},
   "message": "payouts: instant payouts", "author": ["Ari Tan", "ari@example.com"]}
  {"id": "storm-1", "after_calls": 25, "after_s": 900, "action": "storm", "calls": 12,
   "kinds": ["429", "503", "cut", "trickle"]}
  {"id": "flood", "after_calls": 15, "after_s": 600, "action": "flood", "dst": "logs/worker.log", "mb": 40}
  {"id": "teammate", "after_calls": 45, "after_s": 1500, "action": "append", "dst": "pkg/mod.py",
   "src": "avalanche/teammate.py.txt"}
  {"id": "pm-note", "after_calls": 20, "after_s": 800, "action": "note", "dst": "NOTES.md",
   "text": "..."}

Triggers count the gateway's calls since the phase began (faulted ones
included), so every harness meets an avalanche at the same point of its
own climb. A harness the gateway never sees falls back to `after_s` of
phase wall time. Storms are gateway fault bursts switched on live through
the gateway's control file. In oracle and null modes every avalanche of
the phase fires before the phase starts, so graders are checked against
the whole mountain. What fired is recorded in <private>/avalanches.json.
"""

import json
import os
import random
import shutil
import subprocess
import threading
import time
from pathlib import Path

MAX_FLOOD_MB = 64
LOG_LINE = "{ts} INFO  worker[{pid}] job={job} step={step} state=ok elapsed_ms={ms}\n"


def gateway_calls(log):
    n = 0
    try:
        with open(log) as f:
            for line in f:
                if '"ev": "call"' in line:
                    n += 1
    except OSError:
        pass
    return n


class Mountain:
    def __init__(self, task, ws, priv, gw_log=None, gw_control=None):
        self.task, self.ws, self.priv = task, Path(ws), Path(priv)
        self.dir = Path(task["dir"])
        self.gw_log, self.gw_control = gw_log, gw_control
        self.record_path = self.priv / "avalanches.json"
        self._stop = threading.Event()
        self._thread = None

    def _record(self, entry):
        rows = []
        if self.record_path.exists():
            rows = json.loads(self.record_path.read_text())
        rows.append(entry)
        self.record_path.write_text(json.dumps(rows, indent=1))

    def phase_items(self, phase):
        return [a for a in self.task.get("avalanches") or [] if a.get("phase", 1) == phase]

    # ------------------------------------------------------------ actions

    def fire(self, a, phase, call, elapsed, mode):
        act = a["action"]
        detail = ""
        if act == "drop":
            dst = self.ws / a["dst"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.dir / a["src"], dst)
        elif act == "append":
            # a teammate editing the same checkout: their lines land at the end of a
            # file the harness may be working on; only a write from a stale read loses them
            dst = self.ws / a["dst"]
            text = (self.dir / a["src"]).read_text(encoding="utf-8") if a.get("src") else a["text"]
            with open(dst, "a", encoding="utf-8") as f:
                f.write(text)
        elif act == "note":
            dst = self.ws / a["dst"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            with open(dst, "a", encoding="utf-8") as f:
                f.write(a["text"])
        elif act == "commit":
            name, email = a.get("author") or ["Ari Tan", "ari@example.com"]
            env = dict(os.environ, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email,
                       GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email, GIT_CONFIG_NOSYSTEM="1")
            paths = []
            for rel, src in a["files"].items():
                dst = self.ws / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(self.dir / src, dst)
                paths.append(rel)
            subprocess.run(["git", "add", "--", *paths], cwd=self.ws, env=env, capture_output=True)
            # commit only these paths: the harness's own uncommitted work stays where it is
            p = subprocess.run(["git", "commit", "-q", "--no-verify", "-m", a["message"], "--", *paths],
                               cwd=self.ws, env=env, capture_output=True, text=True)
            detail = (p.stdout + p.stderr)[-200:]
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.ws, capture_output=True, text=True).stdout.strip()
            if p.returncode == 0 and sha:
                detail = f"commit {sha} " + detail
        elif act == "storm":
            if self.gw_control:
                now = gateway_calls(self.gw_log)
                ctl = {"bursts": []}
                if os.path.exists(self.gw_control):
                    ctl = json.loads(Path(self.gw_control).read_text())
                ctl["bursts"].append({"from": now + 1, "to": now + int(a.get("calls", 10)),
                                      "kinds": a.get("kinds") or ["429", "503"]})
                tmp = Path(str(self.gw_control) + ".tmp")
                tmp.write_text(json.dumps(ctl))
                os.replace(tmp, self.gw_control)
                detail = f"calls {now + 1}-{now + int(a.get('calls', 10))}"
            else:
                detail = "no gateway (oracle/null): nothing to do"
        elif act == "flood":
            dst = self.ws / a["dst"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            target = min(int(a.get("mb", 20)), MAX_FLOOD_MB) << 20
            r = random.Random(f"obench1:flood:{self.task['id']}:{a['id']}")
            with open(dst, "a", encoding="utf-8") as f:
                size = 0
                while size < target:
                    line = LOG_LINE.format(ts=f"2026-10-30T{r.randint(0, 23):02d}:{r.randint(0, 59):02d}:"
                                              f"{r.randint(0, 59):02d}Z", pid=r.randint(100, 999),
                                           job=r.randint(1, 99999), step=r.randint(1, 40), ms=r.randint(1, 900))
                    f.write(line)
                    size += len(line)
        else:
            raise ValueError(f"unknown avalanche action {act!r}")
        self._record({"id": a["id"], "action": act, "phase": phase, "call": call,
                      "elapsed_s": round(elapsed, 1), "mode": mode, "detail": detail})

    def fire_all(self, phase, mode):
        for a in self.phase_items(phase):
            self.fire(a, phase, None, 0.0, mode)

    # ---------------------------------------------------------- live mode

    def start(self, phase):
        items = sorted(self.phase_items(phase), key=lambda a: a.get("after_calls", 0))
        if not items:
            return
        base = gateway_calls(self.gw_log) if self.gw_log else 0
        t0 = time.time()

        def loop():
            pending = list(items)
            while pending and not self._stop.wait(1.0):
                calls = (gateway_calls(self.gw_log) if self.gw_log else 0) - base
                elapsed = time.time() - t0
                for a in list(pending):
                    by_calls = calls >= a.get("after_calls", 10 ** 9)
                    by_time = calls == 0 and elapsed >= a.get("after_s", 10 ** 9)
                    if by_calls or by_time:
                        try:
                            self.fire(a, phase, calls, elapsed, "agent")
                        except Exception as e:  # an avalanche that can't fire is logged, not fatal
                            self._record({"id": a["id"], "action": a["action"], "phase": phase,
                                          "error": f"{type(e).__name__}: {e}"[:200]})
                        pending.remove(a)
            for a in pending:
                self._record({"id": a["id"], "action": a["action"], "phase": phase, "fired": False,
                              "detail": "the phase ended first"})

        self._stop.clear()
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self):
        if self._thread:
            self._stop.set()
            self._thread.join(timeout=30)
            self._thread = None


def fired(priv, ident):
    """Graders: did avalanche `ident` hit this cell?"""
    p = Path(priv) / "avalanches.json"
    if not p.exists():
        return False
    return any(r.get("id") == ident and r.get("fired", True) and "error" not in r
               for r in json.loads(p.read_text()))
