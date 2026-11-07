"""Write the OBench1 docs' charts into the docs pages, between <!--CHART:name--> markers.

The charts are plain HTML and inline SVG drawn in the site's own colours (currentColor and the
page's CSS variables), so they follow light and dark mode and stay readable on a phone. The data
is the same as the run-1 PDF's: numbers.json and the watch sheets.

    python3 -I docs_charts.py            # print what would change
    python3 -I docs_charts.py --write    # rewrite the pages
"""
import csv, html, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[1] / "watch" / "ob1-3seed-rc2-20261105"
DOCS = Path.home() / "Desktop/overseer-hq/overseer-site/site/pages/docs/obench1"
NUM = json.loads((HERE / "numbers.json").read_text())
REP, PER = NUM["report"], NUM["per_arm"]
NAME = {"overseer": "Overseer v5", "omp": "omp", "hermes": "Hermes", "dsh": "dsh", "pi": "pi"}
ORDER = sorted(NAME, key=lambda a: -REP[a]["approved"])  # the results table's order
T0 = 1793896153  # first call, 16:29 UTC on 5 Nov
T1 = 1793935293  # last cell, 03:21 UTC on 6 Nov
SPAN = T1 - T0
THROTTLE = (21, 23)  # UTC hours, 5 Nov evening
DOUBLE = (1, 4)  # Go's double-rate window, 6 Nov (the run ended inside it)


def esc(s):
    return html.escape(str(s), quote=True)


def pct(t):
    return 100 * (t - T0) / SPAN


def at_utc(day, hour):
    return int(datetime(2026, 11, day, hour, tzinfo=timezone.utc).timestamp())


def windows_svg(h):
    """Shaded throttling and double-rate windows, in a 0..100 x 0..h viewBox."""
    out = []
    for day, (a, b) in ((5, THROTTLE), (6, DOUBLE)):
        x0, x1 = max(0, pct(at_utc(day, a))), min(100, pct(at_utc(day, b)))
        out.append(f'<rect class="win" x="{x0:.2f}" y="0" width="{x1 - x0:.2f}" height="{h}"/>')
    return "".join(out)


def time_axis():
    ticks = []
    for i, (day, hour) in enumerate(((5, 17), (5, 19), (5, 21), (5, 23), (6, 1), (6, 3))):
        cls = ' class="alt"' if i % 2 else ""  # every other tick hides on a phone
        ticks.append(f'<span{cls} style="left:{pct(at_utc(day, hour)):.2f}%">{hour:02d}:00</span>')
    return f'<div class="taxis" aria-hidden="true">{"".join(ticks)}</div>'


def window_key():
    return ('<p class="key" aria-hidden="true"><span class="sw"></span>Shaded: the provider’s throttling '
            '(21:00–23:00) and Go’s double-rate window (from 01:00)</p>')


def scores():
    rows = []
    for a in ORDER:
        r = REP[a]
        tip = f'{NAME[a]}: approved {r["approved"]:.1f}, 95% interval {r["lo"]:.1f}–{r["hi"]:.1f}, raw {r["raw"]:.1f}'
        rows.append(
            f'<div class="row{" us" if a == "overseer" else ""}" title="{esc(tip)}">'
            f'<span class="nm">{NAME[a]}</span>'
            f'<span class="trk"><span class="bar" style="width:{r["approved"]}%"></span>'
            f'<span class="ci" style="left:{r["lo"]}%;width:{r["hi"] - r["lo"]:.1f}%"></span>'
            f'<span class="raw" style="left:{r["raw"]}%"></span></span>'
            f'<span class="v">{r["approved"]:.1f}</span></div>')
    axis = "".join(f'<span style="left:{v}%">{v}</span>' for v in range(0, 101, 20))
    return (
        '<figure class="chart">\n'
        f'<div class="bars grid">{"".join(rows)}</div>\n'
        f'<div class="vaxis" aria-hidden="true">{axis}</div>\n'
        '<figcaption>Approved score out of 100, higher is better. The thin line is the 95% interval and '
        'the ring is the raw score, before the judges.</figcaption>\n</figure>')


def minibars(title, key, fmt, note):
    vals = {a: PER[a][key] if key in PER[a] else REP[a][key] for a in ORDER}
    top = max(vals.values())
    rows = "".join(
        f'<div class="row{" us" if a == "overseer" else ""}" title="{esc(NAME[a] + ": " + fmt(vals[a]))}">'
        f'<span class="nm">{NAME[a]}</span>'
        f'<span class="trk"><span class="bar" style="width:{100 * vals[a] / top:.1f}%"></span></span>'
        f'<span class="v">{fmt(vals[a])}</span></div>' for a in ORDER)
    return f'<div class="mini"><p class="ttl">{title}</p><div class="bars">{rows}</div><p class="note">{note}</p></div>'


def cost():
    return (
        '<figure class="chart pair">\n'
        + minibars("Spend over the run", "usd", lambda v: f"${v:.2f}", "Lower is cheaper.") + "\n"
        + minibars("Spend per approved point", "usd_point", lambda v: f"${v:.4f}",
                   "Lower is better: cheap and wrong doesn’t look cheap.") + "\n"
        + '</figure>')


def output():
    return (
        '<figure class="chart pair">\n'
        + minibars("Output tokens per answered call", "out_per_call", lambda v: f"{v:,.0f}",
                   "Lower is lighter. Reasoning counts as output.") + "\n"
        + minibars("Output tokens over the run", "out", lambda v: f"{v / 1e6:.2f}M",
                   "Lower is cheaper: output is the dearest token.") + "\n"
        + '</figure>')


def categories():
    cats = NUM["categories"]
    head = "".join(f'<th class="n">{NAME[a]}</th>' for a in ORDER)
    body = []
    for c in cats["order"]:
        s = cats["scores"][c]
        cells = []
        for a in ORDER:
            v = s[a]
            cls = ' class="n hm ok"' if v >= 90 else ' class="n hm"'
            cells.append(f'<td{cls} style="--p:{v}%" title="{esc(f"{NAME[a]}, {c}: {v}%")}">{v}%</td>')
        body.append(f'<tr><td>{c}<span class="label">{s["n"]} task{"s" if s["n"] != 1 else ""}</span></td>{"".join(cells)}</tr>')
    return (
        '<div class="tw"><table class="heat">\n'
        f'  <thead><tr><th>Category</th>{head}</tr></thead>\n  <tbody>\n    '
        + "\n    ".join(body) + '\n  </tbody>\n</table></div>\n'
        '<p class="small">Each figure is the share of the category’s judged tasks where the harness was approved on '
        'all three seeds; higher is better. The darker the cell, the higher the share, and <strong>bold</strong> marks a '
        'reliable category (90% or more).</p>')


def throttling():
    bins = 10 * 60
    nb = SPAN // bins + 1
    count = {a: [0] * nb for a in NAME}
    total = {a: 0 for a in NAME}
    for r in csv.DictReader((W / "calls.csv").open()):
        if r["status"] == "429" and r["how"] == "ok":
            count[r["agent"]][(int(r["t"]) - T0) // bins] += 1
            total[r["agent"]] += 1
    top = max(max(v) for v in count.values())
    order = sorted(NAME, key=lambda a: -total[a])
    rows = []
    for a in order:
        w = 100 / nb
        bars = "".join(
            f'<rect x="{i * w:.3f}" y="{40 - 40 * n / top:.2f}" width="{w * .82:.3f}" height="{40 * n / top:.2f}"/>'
            for i, n in enumerate(count[a]) if n)
        rows.append(
            f'<div class="strip{" us" if a == "overseer" else ""}"><span class="nm">{NAME[a]}</span>'
            f'<svg viewBox="0 0 100 40" preserveAspectRatio="none" role="img" '
            f'aria-label="{esc(f"{NAME[a]}: {total[a]} real 429s over the run")}">'
            f'{windows_svg(40)}<g class="ink">{bars}</g></svg>'
            f'<span class="v">{total[a]}</span></div>')
    return (
        '<figure class="chart">\n<div class="strips">' + "".join(rows) + '</div>\n'
        + '<div class="strips"><div class="strip"><span class="nm"></span>' + time_axis() + '<span class="v"></span></div></div>\n'
        + window_key() + '\n'
        f'<figcaption>Real 429s from the provider in 10-minute bins, one row per harness, all on the same scale '
        f'(the tallest bar is {top}). Fewer is better. The total is on the right.</figcaption>\n</figure>')


def progress():
    ends = sorted(int(r["t_end"]) for r in csv.DictReader((W / "cells.csv").open()))
    pts = ["0,60"] + [f"{pct(t):.2f},{60 - 60 * (i + 1) / len(ends):.2f}" for i, t in enumerate(ends)]
    ticks = "".join(f'<span style="bottom:{100 * v / 405:.1f}%">{v}</span>' for v in (0, 100, 200, 300, 405))
    return (
        '<figure class="chart">\n<div class="line"><div class="yaxis" aria-hidden="true">' + ticks + '</div>'
        '<svg viewBox="0 0 100 60" preserveAspectRatio="none" role="img" '
        'aria-label="Cells finished over the run, from 0 at 16:29 UTC to 405 at 03:21 UTC">'
        f'{windows_svg(60)}<polyline class="ln" points="{" ".join(pts)}"/></svg></div>\n'
        '<div class="strips"><div class="strip"><span class="nm"></span>' + time_axis() + '<span class="v"></span></div></div>\n'
        + window_key() + '\n'
        '<figcaption>Cells finished, all five harnesses together, from the first call at 16:29 UTC to the last cell '
        'at 03:21 UTC. Where the line is steeper, cells were finishing faster.'
        '</figcaption>\n</figure>')


CHARTS = {
    "results.html": {"scores": scores, "cost": cost, "categories": categories},
    "learned.html": {"output": output},
    "incidents.html": {"throttling": throttling},
    "run.html": {"progress": progress},
}

if __name__ == "__main__":
    for page, charts in CHARTS.items():
        f = DOCS / page
        s = f.read_text()
        for name, fn in charts.items():
            pat = re.compile(rf"<!--CHART:{name}-->.*?<!--/CHART:{name}-->", re.S)
            if not pat.search(s):
                sys.exit(f"{page}: no <!--CHART:{name}--> marker")
            s = pat.sub(lambda _: f"<!--CHART:{name}-->\n{fn()}\n<!--/CHART:{name}-->", s)
        if "--write" in sys.argv:
            f.write_text(s)
        print(("wrote " if "--write" in sys.argv else "would write ") + str(f), ", ".join(charts))
