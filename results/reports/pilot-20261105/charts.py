"""Charts for the 2026-11-05 OBench1 pilot report, drawn from the watcher's log sheets.

    uv run --no-project --with matplotlib python -I charts.py

Reads ../../watch/ob1-pilot-20261105/{cells,calls}.csv and runner.log, writes PNGs into ./fig/
and the numbers the text quotes into ./numbers.json.
"""

import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
W = HERE.parent.parent / "watch" / "ob1-pilot-20261105"
FIG = HERE / "fig"
FIG.mkdir(exist_ok=True)
FONTS = Path.home() / "Desktop/overseer-hq/overseer-desktop/apps/desktop/assets/fonts"
for f in FONTS.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

# Overseer light mode (design-language/02-colour.md): the grey page, the dark ink, ink at 62/38/14%.
PAGE, INK = "#D4D2CF", "#171615"
INK2, INK3, RULE = "#5D5B59", "#8E8C8A", "#B9B7B4"
# One fixed hue per harness, in this order everywhere (never by rank). Dark enough for 3:1 on the grey page.
ARMS = ["overseer", "omp", "dsh", "pi", "hermes"]
NAME = {"overseer": "Overseer v5", "omp": "omp", "dsh": "dsh", "pi": "pi", "hermes": "Hermes"}
COL = {"overseer": "#2B4C9A", "omp": "#B04A1E", "dsh": "#0F6E5C", "pi": "#6B3FA0", "hermes": "#7A5C00"}
PRICE = {"in": 0.15, "cache": 0.003, "out": 0.60}
T0 = None

plt.rcParams.update({
    "font.family": "Overseer Sans", "font.weight": "regular", "font.size": 8.5,
    "axes.facecolor": PAGE, "figure.facecolor": PAGE, "savefig.facecolor": PAGE,
    "axes.edgecolor": RULE, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.grid": True, "grid.color": RULE, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True,
    "xtick.major.size": 0, "ytick.major.size": 0, "legend.frameon": False,
})


def usd(p, c, o):
    return ((p - c) * PRICE["in"] + c * PRICE["cache"] + o * PRICE["out"]) / 1e6


def load():
    cells = []
    for r in csv.DictReader((W / "cells.csv").open()):
        wall = re.search(r"wall ([\d.]+)s tok (\d+)", r["runner_line"])
        cells.append({"task": r["task"], "arm": r["agent"], "wall": float(wall[1]), "tok_runner": int(wall[2]),
                      "calls": int(r["calls"]), "prompt": int(r["prompt"]), "cached": int(r["cached"]),
                      "out": int(r["output"]), "usd": float(r["usd"]), "errors": int(r["errors"]),
                      "faults": int(r["faults"]), "peak": int(r["peak_ctx"])})
    calls = [dict(r, t=int(r["t"]), prompt=int(r["prompt"]), cached=int(r["cached"]), output=int(r["output"]),
                  ttfb=float(r["ttfb_s"] or 0), wall=float(r["wall_s"] or 0))
             for r in csv.DictReader((W / "calls.csv").open())]
    report = {}
    for line in (W / "runner.log").read_text().splitlines():
        m = re.match(r"^(dsh|hermes|omp|overseer|pi)\s+([\d.]+)\s+([\d.]+)–\s*([\d.]+)\s+([\d.]+)\s+(\d+)/27\s+(\d+)\s+(\d+)"
                     r"\s+(\d+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)%", line)
        if m:
            report[m[1]] = {"approved": float(m[2]), "lo": float(m[3]), "hi": float(m[4]), "raw": float(m[5]),
                            "solved": int(m[6]), "gates": int(m[7]), "infra": int(m[8]), "usd_point": float(m[10]),
                            "tok_point": int(m[11]), "s_point": float(m[12]), "calls_med": int(m[13]),
                            "cache": float(m[14])}
        m = re.match(r"^(dsh|hermes|omp|overseer|pi)\s+summit not yet: reliable in (\d+)/15.*lowest category (\d+)%", line)
        if m:
            report[m[1]].update(reliable=int(m[2]), lowest=int(m[3]))
    return cells, calls, report


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def label_arms(ax, ys):
    ax.set_yticks(ys)
    ax.set_yticklabels([NAME[a] for a in ARMS])
    for t, a in zip(ax.get_yticklabels(), ARMS):
        t.set_color(INK)
    ax.invert_yaxis()


def chart_scores(report):
    fig, ax = plt.subplots(figsize=(6.3, 2.3))
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        r = report[a]
        ax.barh(y, r["approved"], height=0.5, color=COL[a], zorder=2)
        ax.plot([r["lo"], r["hi"]], [y, y], color=INK, lw=1, zorder=3)
        for x in (r["lo"], r["hi"]):
            ax.plot([x, x], [y - 0.12, y + 0.12], color=INK, lw=1, zorder=3)
        ax.scatter([r["raw"]], [y], s=34, facecolor=PAGE, edgecolor=COL[a], lw=1.6, zorder=4)
        ax.text(1.2, y, f"{r['approved']:.1f}", va="center", ha="left", color=PAGE, fontsize=8)
    label_arms(ax, ys)
    ax.set_xlim(0, 100)
    ax.set_xlabel("score out of 100 (bar: approved, whisker: 95% interval, ring: raw)")
    ax.grid(axis="y", visible=False)
    save(fig, "scores")


def chart_spend(cells, report):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.2), gridspec_kw={"wspace": 0.55})
    ys = range(len(ARMS))
    tot = {a: sum(c["usd"] for c in cells if c["arm"] == a) for a in ARMS}
    vals = []
    for y, a in zip(ys, ARMS):
        a1.barh(y, tot[a], height=0.5, color=COL[a], zorder=2)
        a1.text(tot[a] + 0.015, y, f"${tot[a]:.2f}", va="center", fontsize=8)
        v = tot[a] / (report[a]["approved"] * 27 / 100)  # $ per 100 approved points, from the metered spend
        a2.barh(y, v, height=0.5, color=COL[a], zorder=2)
        a2.text(v + 0.004, y, f"${v:.3f}", va="center", fontsize=8)
        vals.append(v)
    for ax, t in ((a1, "metered spend, 27 tasks"), (a2, "spend per 100 approved points")):
        label_arms(ax, ys)
        ax.set_xlabel(t)
        ax.grid(axis="y", visible=False)
    a1.set_xlim(0, max(tot.values()) * 1.3)
    a2.set_xlim(0, max(vals) * 1.35)
    save(fig, "spend")


def chart_tokens(cells):
    fig, ax = plt.subplots(figsize=(6.3, 2.3))
    ys = range(len(ARMS))
    parts = [("cached input", lambda c: c["cached"], 1.0), ("uncached input", lambda c: c["prompt"] - c["cached"], 0.55),
             ("output", lambda c: c["out"], 0.25)]
    for y, a in zip(ys, ARMS):
        left = 0
        for name, f, alpha in parts:
            v = sum(f(c) for c in cells if c["arm"] == a) / 1e6
            ax.barh(y, v, left=left, height=0.5, color=COL[a], alpha=alpha, zorder=2, edgecolor=PAGE, lw=1.2)
            left += v
        ax.text(left + 0.4, y, f"{left:.1f}M", va="center", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlabel("tokens, millions (solid: cached input, mid: uncached input, light: output)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, max(sum(c["prompt"] + c["out"] for c in cells if c["arm"] == a) for a in ARMS) / 1e6 * 1.15)
    save(fig, "tokens")


def chart_cumulative(calls):
    global T0
    fig, ax = plt.subplots(figsize=(6.3, 2.6))
    T0 = min(c["t"] for c in calls)
    ends = []
    for a in ARMS:
        cs = sorted((c for c in calls if c["agent"] == a), key=lambda c: c["t"])
        xs, ys, run = [0], [0], 0.0
        for c in cs:
            run += usd(c["prompt"], c["cached"], c["output"])
            xs.append((c["t"] - T0) / 3600)
            ys.append(run)
        ax.plot(xs, ys, color=COL[a], lw=2, drawstyle="steps-post", label=NAME[a])
        ends.append([ys[-1], xs[-1], a])
    # direct labels at the line ends, nudged apart where the lines finish close together
    ends.sort()
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 0.055)
    for y, x, a in ends:
        ax.text(3.5, y, NAME[a], color=INK, va="center", fontsize=8)
    ax.legend(loc="upper left", fontsize=7.5, handlelength=1.4)
    ax.set_xlabel("hours since the first model call (04:01 UTC)")
    ax.set_ylabel("metered spend, $")
    ax.set_xlim(0, 3.9)
    save(fig, "cumulative")


def task_order(cells):
    seen = []
    for c in cells:
        if c["task"] not in seen:
            seen.append(c["task"])
    return seen


def chart_heat(cells, key, name, fmt, title):
    tasks = task_order(cells)
    grid = [[next((c[key] for c in cells if c["task"] == t and c["arm"] == a), 0) for a in ARMS] for t in tasks]
    import math
    fig, ax = plt.subplots(figsize=(6.3, 7.4))
    vals = [v for row in grid for v in row if v > 0]
    lo, hi = math.log10(min(vals)), math.log10(max(vals))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("seq", ["#E3E1DD", "#9AA6C4", "#4D639E", "#1C2C5A"])
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            s = (math.log10(v) - lo) / (hi - lo) if v > 0 else 0
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=cmap(s), lw=0))
            ax.text(j + 0.5, i + 0.5, fmt(v), ha="center", va="center", fontsize=6.8,
                    color=PAGE if s > 0.55 else INK)
    ax.set_xlim(0, len(ARMS))
    ax.set_ylim(len(tasks), 0)
    ax.set_xticks([j + 0.5 for j in range(len(ARMS))])
    ax.set_xticklabels([NAME[a] for a in ARMS])
    ax.xaxis.tick_top()
    ax.set_yticks([i + 0.5 for i in range(len(tasks))])
    ax.set_yticklabels(tasks, fontsize=7.2)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=8.5, color=INK2, pad=22, loc="left")
    save(fig, name)


def chart_gantt(cells, calls):
    tasks = task_order(cells)
    first = {t: min(c["t"] for c in calls if c["task"] == t) for t in tasks}
    fig, ax = plt.subplots(figsize=(6.3, 2.5))
    for j, a in enumerate(ARMS):
        for c in cells:
            if c["arm"] != a:
                continue
            s = (first[c["task"]] - T0) / 3600
            ax.barh(j, c["wall"] / 3600, left=s, height=0.62, color=COL[a], edgecolor=PAGE, lw=0.6, zorder=2)
    for t in tasks:
        ax.axvline((first[t] - T0) / 3600, color=RULE, lw=0.5, zorder=1)
    label_arms(ax, range(len(ARMS)))
    ax.set_xlabel("hours since 04:01 UTC (one block per task; thin lines: each task's start)")
    ax.grid(False)
    ax.set_xlim(0, 3.5)
    save(fig, "lockstep")


def chart_ttfb(calls):
    fig, ax = plt.subplots(figsize=(6.3, 2.0))
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        v = [c["ttfb"] for c in calls if c["agent"] == a and c["status"] == "200"]
        q = statistics.quantiles(v, n=10)
        med = statistics.median(v)
        ax.plot([q[0], q[8]], [y, y], color=COL[a], lw=1.2, zorder=2)
        ax.scatter([med], [y], s=40, color=COL[a], zorder=3)
        ax.text(q[8] + 0.05, y, f"median {med:.1f}s", va="center", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlabel("seconds to the first byte of each answer (dot: median, line: 10th to 90th percentile)")
    ax.grid(axis="y", visible=False)
    save(fig, "ttfb")


def chart_route():
    fig, ax = plt.subplots(figsize=(6.3, 2.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.6, 4.3)
    ax.axis("off")

    def box(x, y, w, h, text, ec=INK, size=7.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=PAGE, ec=ec, lw=1))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, linespacing=1.2)

    for i, a in enumerate(ARMS):
        y = 3.6 - i * 0.78
        box(0.1, y, 1.6, 0.52, NAME[a], ec=COL[a])
        ax.add_patch(FancyArrowPatch((1.75, y + 0.26), (3.05, 2.25), arrowstyle="-|>", mutation_scale=8,
                                     color=INK3, lw=0.8))
    box(3.1, 0.8, 3.5, 2.95, "cell gateway, one per cell\n\nmodel: deepseek-v4.1-flash\nthinking on, effort max\n"
        "output ceiling 384,000\n\nmeters every call and injects\nthe task's own faults")
    ax.add_patch(FancyArrowPatch((6.65, 2.25), (7.35, 2.25), arrowstyle="-|>", mutation_scale=9, color=INK, lw=1))
    box(7.4, 1.6, 2.5, 1.3, "OpenCode Go\nzen/go/v1")
    save(fig, "route")


def main():
    cells, calls, report = load()
    chart_scores(report)
    chart_spend(cells, report)
    chart_tokens(cells)
    chart_cumulative(calls)
    chart_gantt(cells, calls)
    chart_ttfb(calls)
    chart_route()
    chart_heat(cells, "wall", "heat-wall", lambda v: f"{v / 60:.1f}" if v >= 60 else f"{v:.0f}s",
               "wall time per task, minutes (under a minute: seconds)")
    chart_heat(cells, "tok_runner", "heat-tokens", lambda v: f"{v / 1e6:.2f}M" if v >= 1e6 else f"{v / 1e3:.0f}K",
               "tokens per task (input and output, as each harness counted them)")
    per = {}
    for a in ARMS:
        cs = [c for c in cells if c["arm"] == a]
        p, ca, o = sum(c["prompt"] for c in cs), sum(c["cached"] for c in cs), sum(c["out"] for c in cs)
        per[a] = {"cells": len(cs), "calls": sum(c["calls"] for c in cs), "errors": sum(c["errors"] for c in cs),
                  "faults": sum(c["faults"] for c in cs), "prompt": p, "cached": ca, "out": o, "usd": usd(p, ca, o),
                  "wall_h": sum(c["wall"] for c in cs) / 3600, "peak": max(c["peak"] for c in cs),
                  "longest": max(cs, key=lambda c: c["wall"])["task"], "longest_s": max(c["wall"] for c in cs),
                  "capped": [c["task"] for c in cs if c["wall"] >= 899.5 and c["task"].startswith("ver-")]}
    tasks = task_order(cells)
    first = {t: min(c["t"] for c in calls if c["task"] == t) for t in tasks}
    slowest = {t: max((c for c in cells if c["task"] == t), key=lambda c: c["wall"])["arm"] for t in tasks}
    out = {"per_arm": per, "report": report, "calls": len(calls), "span_h": (max(c["t"] for c in calls) - T0) / 3600,
           "slowest_count": {a: sum(1 for t in tasks if slowest[t] == a) for a in ARMS},
           "non200": sum(1 for c in calls if c["status"] != "200"), "tasks": tasks}
    (HERE / "numbers.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({a: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()} for a, d in per.items()}, indent=0))
    print("slowest", out["slowest_count"], "non200", out["non200"], "span", round(out["span_h"], 2))


if __name__ == "__main__":
    main()
