"""Charts for the OBench1 three-seed run report (ob1-3seed-rc2-20261105), drawn from the watcher's log sheets.

    uv run --no-project --with matplotlib python -I charts.py

Reads ../../watch/ob1-3seed-rc2-20261105/{cells,calls}.csv and runner.log, writes PNGs into ./fig/
and the numbers the text quotes into ./numbers.json. Blind: suite totals and run-level series only.
No chart shows a single task, so nothing here reveals which task a harness failed or gave up on.
"""

import csv
import json
import re
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = "ob1-3seed-rc2-20261105"
W = HERE.parent.parent / "watch" / RUN
FIG = HERE / "fig"
FIG.mkdir(exist_ok=True)
FONTS = Path.home() / "Desktop/overseer-hq/overseer-desktop/apps/desktop/assets/fonts"
for f in FONTS.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

# Overseer light mode (design-language/02-colour.md): the grey page, the dark ink, ink at 62/38/14%.
PAGE, INK = "#D4D2CF", "#171615"
INK2, INK3, RULE, WASH = "#5D5B59", "#8E8C8A", "#B9B7B4", "#C9C7C3"
# One fixed hue per harness, in this order everywhere (never by rank). Same hues as the pilot report.
ARMS = ["overseer", "omp", "dsh", "pi", "hermes"]
NAME = {"overseer": "Overseer v5", "omp": "omp", "dsh": "dsh", "pi": "pi", "hermes": "Hermes"}
COL = {"overseer": "#2B4C9A", "omp": "#B04A1E", "dsh": "#0F6E5C", "pi": "#6B3FA0", "hermes": "#7A5C00"}
PRICE = {"in": 0.15, "cache": 0.003, "out": 0.60}

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


def utc(ts):
    return datetime.fromtimestamp(ts, timezone.utc)


def load():
    cells = [{"task": r["task"], "arm": r["agent"], "seed": int(r["seed"]), "t_end": int(r["t_end"]),
              "wall": float(r["wall_s"]), "calls": int(r["calls"]), "answered": int(r["answered"]),
              "errors": int(r["errors"]), "faults": int(r["faults"]), "prompt": int(r["prompt"]),
              "cached": int(r["cached"]), "out": int(r["output"]), "usd": float(r["usd"] or 0),
              "peak": int(r["peak_ctx"])}
             for r in csv.DictReader((W / "cells.csv").open())]
    calls = [dict(r, t=int(r["t"]), prompt=int(r["prompt"]), cached=int(r["cached"]), output=int(r["output"]),
                  ttfb=float(r["ttfb_s"] or 0), wall=float(r["wall_s"] or 0))
             for r in csv.DictReader((W / "calls.csv").open())]
    report = {}
    for line in (W / "runner.log").read_text().splitlines():
        m = re.match(r"^(dsh|hermes|omp|overseer|pi)\s+([\d.]+)\s+([\d.]+)–\s*([\d.]+)\s+([\d.]+)\s+(\d+)/(\d+)\s+(\d+)"
                     r"\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)%\s+([\d.]+)%", line)
        if m:
            report[m[1]] = {"approved": float(m[2]), "lo": float(m[3]), "hi": float(m[4]), "raw": float(m[5]),
                            "solved": int(m[6]), "cells": int(m[7]), "gates": int(m[8]), "infra": int(m[9]),
                            "usd_point": float(m[11]), "tok_point": int(m[12]), "s_point": float(m[13]),
                            "calls_med": int(m[14]), "cache": float(m[15]), "steady": float(m[16])}
        m = re.match(r"^(dsh|hermes|omp|overseer|pi)\s+summit not yet: reliable in (\d+)/15.*lowest category (\d+)%", line)
        if m:
            report[m[1]].update(reliable=int(m[2]), lowest=int(m[3]))
    assert set(report) == set(ARMS) and all("reliable" in r for r in report.values()), "report lines not parsed"
    return cells, calls, report


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def label_arms(ax, ys):
    ax.set_yticks(list(ys))
    ax.set_yticklabels([NAME[a] for a in ARMS])
    for t in ax.get_yticklabels():
        t.set_color(INK)
    ax.invert_yaxis()


def hours(t, t0):
    return (t - t0) / 3600


def windows(ax, t0, top):
    """Shade Go's 01:00-04:00 UTC double-rate window and the 21:00-23:00 throttling."""
    day = utc(t0).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    thr = (hours(day + 21 * 3600, t0), hours(day + 23 * 3600, t0))
    dbl = (hours(day + 25 * 3600, t0), hours(day + 28 * 3600, t0))
    for (a, b), text in ((thr, "throttling"), (dbl, "Go double rate")):
        ax.axvspan(a, b, color=WASH, lw=0, zorder=0)
        ax.text((a + b) / 2, top, text, ha="center", va="top", fontsize=7, color=INK2)


def xticks_utc(ax, t0, span_h):
    start = utc(t0)
    first = 1 - (start.minute * 60 + start.second) / 3600  # the next whole hour
    xs = [first + i for i in range(0, int(span_h) + 1) if first + i <= span_h]
    ax.set_xticks(xs[::2])
    ax.set_xticklabels([f"{(start.hour + 1 + i) % 24:02d}:00" for i in range(0, len(xs), 2)])


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
    ax.set_xlabel("score out of 100, higher is better (bar: approved, whisker: 95% interval, ring: raw)")
    ax.grid(axis="y", visible=False)
    save(fig, "scores")


def chart_reliable(report):
    fig, ax = plt.subplots(figsize=(6.3, 1.9))
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        n = report[a]["reliable"]
        for k in range(15):
            ax.add_patch(plt.Rectangle((k + 0.08, y - 0.28), 0.84, 0.56, lw=0, zorder=2,
                                       color=COL[a] if k < n else WASH))
        ax.text(15.3, y, f"{n}/15", va="center", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlim(0, 16.4)
    ax.set_ylim(len(ARMS) - 0.5, -0.5)
    ax.set_xticks([])
    ax.grid(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("reliable categories, more is better (a category is reliable when approved on every seed in "
                  "at least 90% of its tasks; order of squares means nothing)")
    save(fig, "reliable")


def chart_spend(cells, report):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.2), gridspec_kw={"wspace": 0.55})
    ys = range(len(ARMS))
    tot = {a: sum(c["usd"] for c in cells if c["arm"] == a) for a in ARMS}
    for y, a in zip(ys, ARMS):
        a1.barh(y, tot[a], height=0.5, color=COL[a], zorder=2)
        a1.text(tot[a] + 0.03, y, f"${tot[a]:.2f}", va="center", fontsize=8)
        v = report[a]["usd_point"]
        a2.barh(y, v, height=0.5, color=COL[a], zorder=2)
        a2.text(v + 0.00002, y, f"${v:.4f}", va="center", fontsize=8)
    for ax, t in ((a1, "metered spend, 81 cells each (lower is cheaper)"), (a2, "spend per approved point, lower is better")):
        label_arms(ax, ys)
        ax.set_xlabel(t)
        ax.grid(axis="y", visible=False)
    a1.set_xlim(0, max(tot.values()) * 1.3)
    a2.set_xlim(0, max(report[a]["usd_point"] for a in ARMS) * 1.35)
    a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.4f}".rstrip("0").rstrip(".")))
    save(fig, "spend")


def chart_tokens(cells):
    fig, ax = plt.subplots(figsize=(6.3, 2.3))
    ys = range(len(ARMS))
    parts = [(lambda c: c["cached"], 1.0), (lambda c: c["prompt"] - c["cached"], 0.55), (lambda c: c["out"], 0.25)]
    tops = []
    for y, a in zip(ys, ARMS):
        left = 0
        for f, alpha in parts:
            v = sum(f(c) for c in cells if c["arm"] == a) / 1e6
            ax.barh(y, v, left=left, height=0.5, color=COL[a], alpha=alpha, zorder=2, edgecolor=PAGE, lw=1.2)
            left += v
        ax.text(left + 0.8, y, f"{left:.0f}M", va="center", fontsize=8)
        tops.append(left)
    label_arms(ax, ys)
    ax.set_xlabel("tokens, millions; fewer is cheaper (solid: cached input, mid: uncached input, light: output)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, max(tops) * 1.15)
    save(fig, "tokens")


def chart_output(cells):
    fig, ax = plt.subplots(figsize=(6.3, 2.0))
    ys = range(len(ARMS))
    vals = {}
    for y, a in zip(ys, ARMS):
        cs = [c for c in cells if c["arm"] == a]
        v = sum(c["out"] for c in cs) / sum(c["answered"] for c in cs)
        vals[a] = v
        ax.barh(y, v, height=0.5, color=COL[a], zorder=2)
        ax.text(v + 12, y, f"{v:.0f}", va="center", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlim(0, max(vals.values()) * 1.18)
    ax.set_xlabel("output tokens per answered call, reasoning and reply together (lower is cheaper)")
    ax.grid(axis="y", visible=False)
    save(fig, "output")
    return vals


def chart_cumulative(calls, t0, span):
    fig, ax = plt.subplots(figsize=(6.3, 2.7))
    ends = []
    top = 0
    for a in ARMS:
        cs = sorted((c for c in calls if c["agent"] == a), key=lambda c: c["t"])
        xs, ys, run = [0], [0], 0.0
        for c in cs:
            run += usd(c["prompt"], c["cached"], c["output"])
            xs.append(hours(c["t"], t0))
            ys.append(run)
        ax.plot(xs, ys, color=COL[a], lw=2, drawstyle="steps-post", zorder=3)
        ends.append([ys[-1], a])
        top = max(top, ys[-1])
    windows(ax, t0, top * 1.12)
    ends.sort()
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + top * 0.06)
    for y, a in ends:
        ax.text(span + 0.15, y, NAME[a], color=INK, va="center", fontsize=8)
    ax.set_xlim(0, span)
    ax.set_ylim(0, top * 1.14)
    xticks_utc(ax, t0, span)
    ax.set_xlabel("time, UTC (5 to 6 November)")
    ax.set_ylabel("metered spend, $ (lower is cheaper)")
    save(fig, "cumulative")


def chart_progress(cells, t0, span):
    fig, ax = plt.subplots(figsize=(6.3, 2.4))
    done = defaultdict(int)
    for c in cells:
        done[(c["task"], c["seed"])] = max(done[(c["task"], c["seed"])], c["t_end"])
    ts = sorted(done.values())
    ax.plot([0] + [hours(t, t0) for t in ts], list(range(len(ts) + 1)), color=INK, lw=1.6,
            drawstyle="steps-post", zorder=3)
    windows(ax, t0, 88)
    ax.set_xlim(0, span)
    ax.set_ylim(0, 90)
    xticks_utc(ax, t0, span)
    ax.set_xlabel("time, UTC")
    ax.set_ylabel("tasks × seeds\nfinished (of 81)")
    save(fig, "progress")


def chart_429(calls, t0, span):
    fig, ax = plt.subplots(figsize=(6.3, 2.4))
    bin_s = 600
    nb = int(span * 3600 // bin_s) + 1
    real = defaultdict(lambda: [0] * nb)
    total = [0] * nb
    for c in calls:
        b = int((c["t"] - t0) // bin_s)
        total[b] += 1
        if c["status"] == "429" and c["how"] == "ok":
            real[c["agent"]][b] += 1
    xs = [(i + 0.5) * bin_s / 3600 for i in range(nb)]
    bottom = [0] * nb
    for a in ARMS:
        ax.bar(xs, real[a], bottom=bottom, width=bin_s / 3600 * 0.9, color=COL[a], zorder=2, lw=0, label=NAME[a])
        bottom = [b + v for b, v in zip(bottom, real[a])]
    top = max(bottom) * 1.15
    windows(ax, t0, top)
    ax.set_xlim(0, span)
    ax.set_ylim(0, top * 1.02)
    xticks_utc(ax, t0, span)
    ax.set_xlabel("time, UTC (10-minute bins)")
    ax.set_ylabel("real 429s (fewer is better)")
    ax.legend(loc="upper left", fontsize=7.5, handlelength=1.0, ncol=1, bbox_to_anchor=(0.01, 0.98))
    save(fig, "ratelimits")
    worst = max(range(nb), key=lambda i: bottom[i])
    return {"worst_bin_utc": utc(t0 + worst * bin_s).strftime("%H:%M"), "worst_bin_429": bottom[worst],
            "worst_bin_calls": total[worst]}


def chart_ttfb(calls):
    fig, ax = plt.subplots(figsize=(6.3, 2.0))
    ys = range(len(ARMS))
    med = {}
    for y, a in zip(ys, ARMS):
        v = [c["ttfb"] for c in calls if c["agent"] == a and c["status"] == "200"]
        q = statistics.quantiles(v, n=10)
        med[a] = statistics.median(v)
        ax.plot([q[0], q[8]], [y, y], color=COL[a], lw=1.2, zorder=2)
        ax.scatter([med[a]], [y], s=40, color=COL[a], zorder=3)
        ax.text(q[8] + 0.08, y, f"median {med[a]:.1f}s", va="center", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlabel("seconds to the first byte of each answer, lower is faster; this is the provider, not the harness\n(dot: median, line: 10th to 90th percentile)")
    ax.grid(axis="y", visible=False)
    save(fig, "ttfb")
    return med


def load_categories():
    """Per-category share, from report --by-category (the owner lifted the blind rule on 2026-11-06)."""
    cats, order, arm = defaultdict(dict), [], None
    for line in (W / "report-by-category.txt").read_text().splitlines():
        m = re.match(r"^(dsh|hermes|omp|overseer|pi)\s+summit", line)
        if m:
            arm = m[1]
            continue
        m = re.match(r"^\s{4}(\S.*?)\s{2,}(\d+)%\s+\((\d+) tasks?\)", line)
        if m and arm:
            name = m[1].replace("Resilience: provider faults and mid-run changes", "Resilience")
            if name not in order:
                order.append(name)
            cats[name][arm] = int(m[2])
            cats[name]["n"] = int(m[3])
    assert len(order) == 15 and all(len(cats[c]) == 6 for c in order), "category report not parsed"
    return order, cats


SEQ = ["#E3E1DD", "#9AA6C4", "#4D639E", "#1C2C5A"]


def chart_categories(order, cats):
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    fig, ax = plt.subplots(figsize=(6.3, 5.0))
    for i, c in enumerate(order):
        for j, a in enumerate(ARMS):
            v = cats[c][a]
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=cmap(v / 100), lw=0))
            if v >= 90:
                ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, fill=False, ec=INK, lw=1.1))
            ax.text(j + 0.5, i + 0.5, f"{v}%", ha="center", va="center", fontsize=7.6,
                    color=PAGE if v > 55 else INK)
    ax.set_xlim(0, len(ARMS))
    ax.set_ylim(len(order), 0)
    ax.set_xticks([j + 0.5 for j in range(len(ARMS))])
    ax.set_xticklabels([NAME[a] for a in ARMS])
    for t in ax.get_xticklabels():
        t.set_color(INK)
    ax.xaxis.tick_top()
    ax.set_yticks([i + 0.5 for i in range(len(order))])
    ax.set_yticklabels([f"{c} ({cats[c]['n']})" for c in order], fontsize=7.6)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("share of the category's tasks approved on all three seeds, higher is better; outlined: reliable "
                  "(90% or more); in brackets: tasks the category judged", fontsize=7.2)
    save(fig, "categories")


def chart_cat_gap(order, cats):
    fig, ax = plt.subplots(figsize=(6.3, 3.9))
    others = [a for a in ARMS if a != "overseer"]
    for i, c in enumerate(order):
        best = max(cats[c][a] for a in others)
        who = [NAME[a] for a in others if cats[c][a] == best]
        d = cats[c]["overseer"] - best
        if d:
            ax.barh(i, d, height=0.55, color=COL["overseer"] if d > 0 else INK3, zorder=2)
        else:
            ax.scatter([0], [i], s=18, color=INK2, zorder=3)
        txt = f"{d:+d} vs {', '.join(who) if len(who) < 4 else 'all four'}" if d else \
            f"level with {', '.join(who) if len(who) < 4 else 'all four'}"
        ax.text(d + (1.5 if d >= 0 else -1.5), i, txt, va="center", ha="left" if d >= 0 else "right",
                fontsize=7.2, color=INK2)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=7.6)
    for t in ax.get_yticklabels():
        t.set_color(INK)
    ax.invert_yaxis()
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-40, 105)
    ax.set_xlabel("Overseer v5's category score minus the best of the other four, in points (right of 0: v5 ahead)")
    ax.grid(axis="y", visible=False)
    save(fig, "category-gap")


PILOT = {"omp": 51.6, "pi": 40.5, "hermes": 36.8, "dsh": 29.6, "overseer": 29.6}


def chart_pilot(report):
    fig, ax = plt.subplots(figsize=(6.3, 2.2))
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        p, f = PILOT[a], report[a]["approved"]
        void = a == "overseer"
        ax.plot([p, f], [y, y], color=RULE, lw=1.4, zorder=1, ls=(0, (2, 2)) if void else "-")
        ax.scatter([p], [y], s=30, facecolor=PAGE, edgecolor=INK3 if void else COL[a], lw=1.4, zorder=3)
        ax.scatter([f], [y], s=42, color=COL[a], zorder=3)
        up = f >= p
        ax.text(p + (-1.5 if up else 1.5), y, "pilot void" if void else f"{p:.1f}", va="center",
                ha="right" if up else "left", fontsize=7.4, color=INK2)
        ax.text(f + (1.5 if up else -1.5), y, f"{f:.1f}", va="center", ha="left" if up else "right", fontsize=8)
    label_arms(ax, ys)
    ax.set_xlim(0, 100)
    ax.set_xlabel("approved score, higher is better: ring, the one-seed pilot (5 Nov 04:01); dot, this three-seed run")
    ax.grid(axis="y", visible=False)
    save(fig, "pilot-vs-final")


def chart_hourly(calls, t0, span):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.3, 3.6), sharex=True, gridspec_kw={"hspace": 0.18,
                                                                                    "height_ratios": [3, 2]})
    bin_s = 1200
    nb = int(span * 3600 // bin_s) + 1
    xs = [(i + 0.5) * bin_s / 3600 for i in range(nb)]
    per = defaultdict(lambda: [0] * nb)
    tot, lim = [0] * nb, [0] * nb
    for c in calls:
        b = int((c["t"] - t0) // bin_s)
        per[c["agent"]][b] += 1
        tot[b] += 1
        lim[b] += c["status"] == "429" and c["how"] == "ok"
    top = 0
    for a in ARMS:
        a1.plot(xs, per[a], color=COL[a], lw=1.5, label=NAME[a], zorder=3)
        top = max(top, max(per[a]))
    windows(a1, t0, top * 1.22)
    a1.set_ylim(0, top * 1.25)
    a1.set_ylabel("model calls per 20 min")
    a1.legend(loc="lower left", fontsize=7.2, ncol=5, handlelength=1.2, bbox_to_anchor=(0, 1.0))
    share = [100 * l / t if t else 0 for l, t in zip(lim, tot)]
    a2.fill_between(xs, share, color=INK2, lw=0, alpha=0.35, zorder=2)
    a2.plot(xs, share, color=INK, lw=1.2, zorder=3)
    windows(a2, t0, 48)
    a2.set_ylim(0, 50)
    a2.set_ylabel("% of calls rate-\nlimited (lower is better)")
    a2.set_xlim(0, span)
    xticks_utc(a2, t0, span)
    a2.set_xlabel("time, UTC; every call from every harness, real 429s only (injected faults are not in this log)")
    save(fig, "hourly")


def chart_cache_calls(report):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.1), gridspec_kw={"wspace": 0.55})
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        r = report[a]
        a1.barh(y, r["cache"], height=0.5, color=COL[a], zorder=2)
        a1.text(r["cache"] + 0.4, y, f"{r['cache']:.1f}%", va="center", fontsize=8)
        a2.barh(y, r["calls_med"], height=0.5, color=COL[a], zorder=2)
        a2.text(r["calls_med"] + 0.3, y, str(r["calls_med"]), va="center", fontsize=8)
    for ax, t in ((a1, "input served from cache, higher is cheaper"), (a2, "model calls in a typical cell (median; context, not a score)")):
        label_arms(ax, ys)
        ax.set_xlabel(t)
        ax.grid(axis="y", visible=False)
    a1.set_xlim(80, 100)
    a2.set_xlim(0, max(report[a]["calls_med"] for a in ARMS) * 1.3)
    save(fig, "cache-calls")


def chart_time(per, slow, n):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.1), gridspec_kw={"wspace": 0.55})
    ys = range(len(ARMS))
    for y, a in zip(ys, ARMS):
        a1.barh(y, per[a]["busy_h"], height=0.5, color=COL[a], zorder=2)
        a1.text(per[a]["busy_h"] + 0.15, y, f"{per[a]['busy_h']:.1f} h", va="center", fontsize=8)
        a2.barh(y, slow[a], height=0.5, color=COL[a], zorder=2)
        a2.text(slow[a] + 0.6, y, f"{slow[a]} of {n}", va="center", fontsize=8)
    for ax, t in ((a1, "busy time, all 81 cells added up (lower is faster)"), (a2, "times it was last to finish, lower is better")):
        label_arms(ax, ys)
        ax.set_xlabel(t)
        ax.grid(axis="y", visible=False)
    a1.set_xlim(0, 12.5)
    a2.set_xlim(0, max(slow.values()) * 1.45)
    save(fig, "time")


def chart_heat(cells, key, name, fmt, title):
    """Median over the three seeds, per task and harness."""
    import math
    from matplotlib.colors import LinearSegmentedColormap
    tasks = []
    for c in cells:
        if c["task"] not in tasks:
            tasks.append(c["task"])
    grid = [[statistics.median([key(c) for c in cells if c["task"] == t and c["arm"] == a]) for a in ARMS]
            for t in tasks]
    fig, ax = plt.subplots(figsize=(6.3, 7.4))
    vals = [v for row in grid for v in row if v > 0]
    lo, hi = math.log10(min(vals)), math.log10(max(vals))
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
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


def chart_route():
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.35, 4.3)
    ax.axis("off")

    def box(x, y, w, h, text, ec=INK, size=7.8, ls="-"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=PAGE, ec=ec,
                                    lw=1, ls=ls))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, linespacing=1.2)

    ax.add_patch(FancyBboxPatch((0.0, 0.45), 6.75, 3.8, boxstyle="round,pad=0.02,rounding_size=0.15", fc="none",
                                ec=INK3, lw=0.8, ls=(0, (3, 2))))
    ax.text(0.12, 0.56, "the jail: loopback only, no apps, no Apple Events, no window server", fontsize=7,
            color=INK2, va="bottom")
    for i, a in enumerate(ARMS):
        y = 3.6 - i * 0.7
        box(0.15, y, 1.6, 0.48, NAME[a], ec=COL[a])
        ax.add_patch(FancyArrowPatch((1.8, y + 0.24), (3.05, 2.35), arrowstyle="-|>", mutation_scale=8,
                                     color=INK3, lw=0.8))
    box(3.1, 0.95, 3.5, 2.85, "cell gateway, one per cell\n\nmodel: deepseek-v4.1-flash\nthinking on, effort max\n"
        "output ceiling 384,000\n\nmeters every call and injects\nthe task's own faults")
    ax.add_patch(FancyArrowPatch((6.65, 2.35), (7.35, 2.35), arrowstyle="-|>", mutation_scale=9, color=INK, lw=1))
    box(7.4, 1.7, 2.5, 1.3, "OpenCode Go\nzen/go/v1")
    save(fig, "route")


def main():
    cells, calls, report = load()
    assert len(cells) == 405, len(cells)
    t0 = min(c["t"] for c in calls)
    t1 = max(max(c["t"] for c in calls), max(c["t_end"] for c in cells))
    span = hours(t1, t0)
    chart_scores(report)
    chart_reliable(report)
    chart_spend(cells, report)
    chart_tokens(cells)
    out_call = chart_output(cells)
    chart_cumulative(calls, t0, span)
    chart_progress(cells, t0, span)
    worst = chart_429(calls, t0, span)
    ttfb = chart_ttfb(calls)
    chart_route()

    per = {}
    for a in ARMS:
        cs = [c for c in cells if c["arm"] == a]
        ks = [c for c in calls if c["agent"] == a]
        p, ca, o = sum(c["prompt"] for c in cs), sum(c["cached"] for c in cs), sum(c["out"] for c in cs)
        per[a] = {"cells": len(cs), "calls": len(ks), "answered": sum(c["answered"] for c in cs),
                  "real429": sum(1 for c in ks if c["status"] == "429" and c["how"] == "ok"),
                  "other_err": sum(1 for c in ks if c["status"] not in ("200", "429")),
                  "faults": sum(c["faults"] for c in cs), "prompt": p, "cached": ca, "out": o,
                  "usd": sum(c["usd"] for c in cs), "busy_h": sum(c["wall"] for c in cs) / 3600,
                  "peak": max(c["peak"] for c in cs), "out_per_call": out_call[a], "ttfb_med": ttfb[a]}
    # slowest arm per task and seed: an aggregate count, no task named
    slow = defaultdict(int)
    groups = defaultdict(list)
    for c in cells:
        groups[(c["task"], c["seed"])].append(c)
    for g in groups.values():
        slow[max(g, key=lambda c: c["wall"])["arm"]] += 1
    dead = {a: sum(1 for c in cells if c["arm"] == a and c["answered"] == 0) for a in ARMS}
    status = defaultdict(int)
    for c in calls:
        status[f"{c['status']} {c['how']}"] += 1
    order, cats = load_categories()
    chart_categories(order, cats)
    chart_cat_gap(order, cats)
    chart_pilot(report)
    chart_hourly(calls, t0, span)
    chart_cache_calls(report)
    chart_time(per, slow, len(groups))
    chart_heat(cells, lambda c: c["wall"], "heat-wall", lambda v: f"{v / 60:.1f}" if v >= 60 else f"{v:.0f}s",
               "wall time per task, median of three seeds, minutes (under a minute: seconds); lighter is faster")
    chart_heat(cells, lambda c: c["prompt"] + c["out"], "heat-tokens",
               lambda v: "none" if v == 0 else f"{v / 1e6:.2f}M" if v >= 1e6 else f"{v / 1e3:.0f}K",
               "tokens per task, input and output, median of three seeds; lighter is fewer; none: no call was answered")
    out = {"categories": {"order": order, "scores": cats}, "per_arm": per, "report": report, "calls": len(calls),
           "span_h": span,
           "t0_utc": utc(t0).strftime("%Y-%m-%d %H:%M:%S"), "t1_utc": utc(t1).strftime("%Y-%m-%d %H:%M:%S"),
           "slowest_count": {a: slow[a] for a in ARMS}, "task_seeds": len(groups), "status": dict(status),
           "worst_429_bin": worst, "no_answer_cells": dead, "usd_total": sum(c["usd"] for c in cells)}
    (HERE / "numbers.json").write_text(json.dumps(out, indent=1))
    for a in ARMS:
        print(a, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in per[a].items()})
    print({k: v for k, v in out.items() if k not in ("per_arm", "report")})


if __name__ == "__main__":
    main()
