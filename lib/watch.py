"""Run watcher: the log sheets for a field run, written while it climbs.

    python3 lib/watch.py --run-set ID --runner-log FILE --out DIR [--every 30] [--stop-usd N]

Every --every seconds it reads each live cell's gateway log (the metered view
of every model call) and the runner's own log, and writes into --out:

  live.md        the current picture: one row per cell climbing now, per-arm totals
  progress.csv   one row per cell per tick (the time series behind the charts)
  calls.csv      one row per model call once answered (status, tokens, ttfb, wall)
  cells.csv      one row per finished cell (wall, tokens, cost, calls, errors)
  events.log     what deserves a look: starts, finishes, error bursts, stalls,
                 every $1 of spend, provider 429s, cell failures
  arm-<name>.md  one sheet per harness: its cells so far, in order

It never reads grades: scores stay sealed until `obench.py report`. With
--stop-usd it ends the run (SIGTERM to the runner's process group) once metered
spend passes N; without it, it only reports.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import signal
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("OBENCH_WATCH", "1")

STALL_S = 600       # no gateway event for this long while the arm still runs
BURST = 3           # this many non-2xx answers in a row is worth a line
CELL_RE = re.compile(r"^(?P<task>.+)-(?P<agent>[a-z]+(?:_[A-Za-z0-9]+)?)-s(?P<seed>\d+)-[0-9a-f]{6}$")


def price():
    up = os.environ.get("OBENCH_UPSTREAM") or os.environ.get("OVERSEER_BASE_URL") or "https://opencode.ai/zen/go/v1"
    p = {"in": 0.15, "cache": 0.003, "out": 0.60} if "/zen/go" in up else {"in": 0.30, "cache": 0.006, "out": 1.20}
    if os.environ.get("OBENCH_PRICE"):
        p = dict(zip(("in", "cache", "out"), map(float, os.environ["OBENCH_PRICE"].split(","))))
    return p


PRICE = price()


def usd(prompt, cached, out):
    return ((prompt - cached) * PRICE["in"] + cached * PRICE["cache"] + out * PRICE["out"]) / 1e6


class Cell:
    def __init__(self, name, path):
        m = CELL_RE.match(name)
        self.name, self.path = name, path
        self.task, self.agent, self.seed = (m["task"], m["agent"].replace("_", "@"), int(m["seed"])) if m else (name, "?", 0)
        self.t0 = path.stat().st_mtime
        self.pos = 0
        self.calls = self.answered = self.errors = self.faults = self.streak = 0
        self.prompt = self.cached = self.out = 0
        self.peak_ctx = 0
        self.last_t = self.t0
        self.done = False
        self.asked = None
        self.stall_noted = False
        self.dollar_mark = 0

    def read(self, calls_w):
        log = self.path / "gateway.jsonl"
        if not log.exists():
            return []
        news = []
        with log.open() as f:
            f.seek(self.pos)
            for line in f:
                if not line.endswith("\n"):
                    break  # half-written: next tick
                self.pos += len(line.encode())
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                self.last_t = e.get("t", self.last_t)
                self.stall_noted = False
                ev = e.get("ev")
                if ev == "call":
                    self.calls += 1
                    if e.get("fault"):
                        self.faults += 1
                    if e.get("asked") and self.asked is None:
                        self.asked = e["asked"]
                elif ev == "done" and e.get("n"):  # a model call's answer, not a probe passing through
                    p, c, o = e.get("prompt", 0) or 0, e.get("cached", 0) or 0, e.get("output", 0) or 0
                    self.prompt += p
                    self.cached += c
                    self.out += o
                    self.peak_ctx = max(self.peak_ctx, p)
                    ok = 200 <= (e.get("status") or 0) < 300
                    self.answered += ok
                    self.errors += not ok
                    self.streak = 0 if ok else self.streak + 1
                    if self.streak == BURST:
                        news.append(f"{self.label()}: {BURST} failed answers in a row (last status {e.get('status')})")
                    if e.get("status") == 429:
                        news.append(f"{self.label()}: provider 429 on call {e.get('n')}")
                    calls_w.writerow([round(e.get("t", 0)), self.task, self.agent, self.seed, e.get("n"),
                                      e.get("status"), e.get("how"), p, c, o, e.get("ttfb_s"), e.get("wall_s")])
                elif ev == "upstream_error":
                    self.errors += 1
                    news.append(f"{self.label()}: upstream error on call {e.get('n')}: {e.get('error', '')[:120]}")
        return news

    def cost(self):
        return usd(self.prompt, self.cached, self.out)

    def label(self):
        return f"{self.task} / {self.agent} s{self.seed}"

    def row(self, now):
        hit = f"{100 * self.cached / self.prompt:.0f}%" if self.prompt else "-"
        return (f"| {self.task} | {self.agent} | {fmt_s(now - self.t0)} | {self.calls} | {self.errors} | "
                f"{self.prompt / 1e3:,.0f}K | {hit} | {self.out / 1e3:,.1f}K | {self.peak_ctx / 1e3:,.0f}K | "
                f"${self.cost():.3f} | {fmt_s(now - self.last_t)} |")


def fmt_s(s):
    s = int(max(0, s))
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def runner_lines(path, pos):
    if not path.exists():
        return [], pos
    with path.open(errors="replace") as f:
        f.seek(pos)
        data = f.read()
    keep = data.rsplit("\n", 1)
    if len(keep) == 1:
        return [], pos
    return [x for x in keep[0].split("\n") if x.strip()], pos + len(keep[0].encode()) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-set", required=True)
    ap.add_argument("--runner-log", required=True)
    ap.add_argument("--runner-pid", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--every", type=int, default=30)
    ap.add_argument("--stop-usd", type=float)
    a = ap.parse_args()
    import obench  # PROOT, RUNS: the same roots the runner uses
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    start = time.time()
    events = (out / "events.log").open("a", buffering=1)

    def note(msg):
        events.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}Z  {msg}\n")

    def sheet(name, header):
        p = out / name
        new = not p.exists()
        f = p.open("a", newline="", buffering=1)
        w = csv.writer(f)
        if new:
            w.writerow(header)
        return f, w

    _, prog_w = sheet("progress.csv", ["t", "task", "agent", "seed", "elapsed_s", "calls", "answered", "errors",
                                       "faults", "prompt", "cached", "output", "peak_ctx", "usd", "idle_s"])
    _, calls_w = sheet("calls.csv", ["t", "task", "agent", "seed", "n", "status", "how", "prompt", "cached",
                                     "output", "ttfb_s", "wall_s"])
    _, cells_w = sheet("cells.csv", ["t_end", "task", "agent", "seed", "wall_s", "calls", "answered", "errors",
                                     "faults", "prompt", "cached", "output", "peak_ctx", "usd", "runner_line"])
    note(f"watch start: run set {a.run_set}, price/1M in {PRICE['in']} cache {PRICE['cache']} out {PRICE['out']}"
         f"{'' if a.stop_usd is None else f', stop at ${a.stop_usd}'}")
    cells: dict[str, Cell] = {}
    finished: list[Cell] = []
    rpos = 0
    tasks_done = set()
    spent_mark = 0
    stopped = False
    while True:
        now = time.time()
        for d in obench.PROOT.glob("*"):
            if d.name not in cells and d.is_dir() and d.stat().st_mtime >= start - 5 and CELL_RE.match(d.name):
                c = cells[d.name] = Cell(d.name, d)
                note(f"start  {c.label()}")
        for c in cells.values():
            if not c.done:
                for msg in c.read(calls_w):
                    note(msg)
                if c.asked:
                    note(f"{c.label()}: gateway overrode the arm's own request {json.dumps(c.asked)[:200]}")
                    c.asked = {}
                if not c.path.exists() and not c.done:
                    # the private dir is gone: the arm finished and its line is still
                    # queued behind slower arms (the runner prints in launch order)
                    c.ended = True
                if now - c.last_t > STALL_S and not c.stall_noted and not getattr(c, "ended", False):
                    c.stall_noted = True
                    note(f"{c.label()}: no model traffic for {fmt_s(now - c.last_t)} (thinking, a long tool, or a hang)")
                if int(c.cost()) > c.dollar_mark:
                    c.dollar_mark = int(c.cost())
                    note(f"{c.label()}: passed ${c.dollar_mark} on its own")
                prog_w.writerow([round(now), c.task, c.agent, c.seed, round(now - c.t0), c.calls, c.answered,
                                 c.errors, c.faults, c.prompt, c.cached, c.out, c.peak_ctx, round(c.cost(), 5),
                                 round(now - c.last_t)])
        lines, rpos = runner_lines(Path(a.runner_log), rpos)
        for line in lines:
            m = re.match(r"^(\S+)\s+(\S+)\s+s(\d+)\s+(done|CELL FAILED)", line)
            if not m:
                if line.strip():
                    note(f"runner: {line[:300]}")
                continue
            task, agent, seed, what = m[1], m[2], int(m[3]), m[4]
            match = [c for c in cells.values() if c.task == task and c.agent == agent and c.seed == seed and not c.done]
            view = obench.RUNS / a.run_set / task / f"{agent.replace('@', '_')}-s{seed}"
            if not match and (view / "gateway.jsonl").exists():
                # climbed and finished between two ticks: read it whole from the kept copy
                c = cells[f"{task}-{agent}-s{seed}-done"] = Cell(f"{task}-{agent.replace('@', '_')}-s{seed}-000000", view)
                c.t0 = now - float((re.search(r"wall ([\d.]+)s", line) or [0, 0])[1])
                match = [c]
            for c in match[:1]:
                kept = obench.RUNS / a.run_set / c.task / f"{c.agent.replace('@', '_')}-s{c.seed}" / "gateway.jsonl"
                if kept.exists():
                    c.path = kept.parent  # the private dir is gone; finish from the kept copy
                for msg in c.read(calls_w):
                    note(msg)
                c.done = True
                finished.append(c)
                cells_w.writerow([round(now), c.task, c.agent, c.seed, round(now - c.t0), c.calls, c.answered,
                                  c.errors, c.faults, c.prompt, c.cached, c.out, c.peak_ctx, round(c.cost(), 5),
                                  line[:300]])
            note(("FAILED " if what != "done" else "finish ") + line[:300])
            tasks_done.add(task)
        total = sum(c.cost() for c in cells.values())
        if int(total) > spent_mark:
            spent_mark = int(total)
            note(f"spend: ${total:.2f} metered so far")
        live = [c for c in cells.values() if not c.done]
        arms = sorted({c.agent for c in cells.values()})
        md = [f"# {a.run_set}: live",
              f"\nUpdated {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}Z, {fmt_s(now - start)} in. "
              f"Cells finished {len(finished)}, climbing {len(live)}. Metered spend ${total:.2f}.\n",
              "## Climbing now\n",
              "| task | arm | elapsed | calls | errors | input | cached | output | peak ctx | cost | idle |",
              "|---|---|---|---|---|---|---|---|---|---|---|"] + [c.row(now) for c in live] + [
              "\n## Per arm so far\n",
              "| arm | cells | calls | errors | input | cached | output | cost |", "|---|---|---|---|---|---|---|---|"]
        for arm in arms:
            cs = [c for c in cells.values() if c.agent == arm]
            p, ca, o = sum(c.prompt for c in cs), sum(c.cached for c in cs), sum(c.out for c in cs)
            md.append(f"| {arm} | {len(cs)} | {sum(c.calls for c in cs)} | {sum(c.errors for c in cs)} | "
                      f"{p / 1e6:.2f}M | {f'{100 * ca / p:.0f}%' if p else '-'} | {o / 1e3:,.0f}K | "
                      f"${usd(p, ca, o):.2f} |")
            arm_md = [f"# {a.run_set}: {arm}\n", "| task | elapsed | calls | errors | input | cached | output | "
                      "peak ctx | cost | idle |", "|---|---|---|---|---|---|---|---|---|---|"]
            arm_md += [c.row(now).replace(f"| {c.agent} ", "", 1) + (" done" if c.done else " climbing") for c in cs]
            (out / f"arm-{arm.replace('@', '_')}.md").write_text("\n".join(arm_md) + "\n")
        (out / "live.md").write_text("\n".join(md) + "\n")
        if a.stop_usd is not None and total >= a.stop_usd and not stopped and a.runner_pid:
            stopped = True
            note(f"STOP: metered spend ${total:.2f} passed ${a.stop_usd}; ending the run")
            try:
                os.killpg(os.getpgid(a.runner_pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        if a.runner_pid:
            try:
                os.kill(a.runner_pid, 0)
            except ProcessLookupError:
                lines, rpos = runner_lines(Path(a.runner_log), rpos)
                for line in lines:
                    note(f"runner: {line[:300]}")
                note(f"watch end: runner exited; {len(finished)} cells finished, metered spend ${total:.2f}")
                return
        time.sleep(a.every)


if __name__ == "__main__":
    main()
