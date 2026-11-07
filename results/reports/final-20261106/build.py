"""The OBench1 three-seed run report (ob1-3seed-rc2-20261105): prep, fairness, oversight, results and categories.

    uv run --no-project --with matplotlib python -I charts.py
    uv run --no-project --with reportlab --with pillow python -I build.py

Writes obench1-run1-2026-11-06.pdf next to this file. Type and colour follow
overseer-site/design-language (light mode: the grey page, the dark ink; Overseer Display and Sans).
Includes the per-category scores the owner unsealed on 2026-11-06; those aren't public yet.
"""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = Path(__file__).resolve().parent
FONTS = Path.home() / "Desktop/overseer-hq/overseer-desktop/apps/desktop/assets/fonts"
for name in ("OverseerDisplay-Light", "OverseerDisplay-Regular", "OverseerSans-Light", "OverseerSans-Regular",
             "OverseerSans-Medium"):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / f"{name}.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily  # noqa: E402

registerFontFamily("OverseerSans-Regular", normal="OverseerSans-Regular", bold="OverseerSans-Medium",
                   italic="OverseerSans-Regular", boldItalic="OverseerSans-Medium")

PAGE, INK = colors.HexColor("#D4D2CF"), colors.HexColor("#171615")
INK2, INK3, RULE = colors.HexColor("#5D5B59"), colors.HexColor("#8E8C8A"), colors.HexColor("#B9B7B4")
ARMS = ["overseer", "omp", "dsh", "pi", "hermes"]
RANK = ["overseer", "omp", "hermes", "dsh", "pi"]  # table order: by approved score
NAME = {"overseer": "Overseer v5", "omp": "omp", "dsh": "dsh", "pi": "pi", "hermes": "Hermes"}
N = json.loads((HERE / "numbers.json").read_text())
P, R = N["per_arm"], N["report"]
CAT, CATS = N["categories"]["order"], N["categories"]["scores"]
DEAD = N["no_answer_cells"]
W_TEXT = A4[0] - 40 * mm

import sys  # noqa: E402
sys.path.insert(0, str(HERE))
from narratives import ASKS, TEXT  # noqa: E402

S = {
    "title": ParagraphStyle("title", fontName="OverseerDisplay-Light", fontSize=30, leading=34, textColor=INK),
    "sub": ParagraphStyle("sub", fontName="OverseerSans-Regular", fontSize=11.5, leading=16, textColor=INK2),
    "h1": ParagraphStyle("h1", fontName="OverseerDisplay-Regular", fontSize=19, leading=24, textColor=INK,
                         spaceBefore=4, spaceAfter=8, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="OverseerDisplay-Regular", fontSize=13, leading=17, textColor=INK,
                         spaceBefore=10, spaceAfter=4, keepWithNext=1),
    "body": ParagraphStyle("body", fontName="OverseerSans-Regular", fontSize=9.4, leading=13.6, textColor=INK,
                           spaceAfter=6, alignment=TA_LEFT),
    "small": ParagraphStyle("small", fontName="OverseerSans-Regular", fontSize=8, leading=11, textColor=INK2,
                            spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="OverseerSans-Regular", fontSize=8, leading=10.5, textColor=INK),
    "cellsm": ParagraphStyle("cellsm", fontName="OverseerSans-Regular", fontSize=6.6, leading=9, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="OverseerSans-Medium", fontSize=8, leading=10.5, textColor=INK),
    "tile_n": ParagraphStyle("tile_n", fontName="OverseerDisplay-Light", fontSize=22, leading=25, textColor=INK),
    "tile_l": ParagraphStyle("tile_l", fontName="OverseerSans-Regular", fontSize=8, leading=10.5, textColor=INK2),
    "bullet": ParagraphStyle("bullet", fontName="OverseerSans-Regular", fontSize=9.4, leading=13.6, textColor=INK,
                             leftIndent=11, bulletIndent=0, spaceAfter=3),
    "note": ParagraphStyle("note", fontName="OverseerSans-Regular", fontSize=8.6, leading=12.4, textColor=INK,
                           borderColor=INK3, borderWidth=0.6, borderPadding=7, spaceBefore=6, spaceAfter=10),
}


def curly(text):
    """Design language: curly quotes and apostrophes. Leaves markup inside <...> alone."""
    out, depth = [], 0
    for i, ch in enumerate(text):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0 and ch == "'":
            ch = "\u2018" if i == 0 or text[i - 1] in " (\u201c\n" else "\u2019"
        elif depth == 0 and ch == '"':
            ch = "\u201c" if i == 0 or text[i - 1] in " (\n" else "\u201d"
        out.append(ch)
    return "".join(out)


def p(text, style="body"):
    return Paragraph(curly(text), S[style])


def bullets(items):
    return [Paragraph(curly(t), S["bullet"], bulletText="•") for t in items]


def table(rows, widths, head=True):
    data = [[p(c, "cellh" if head and i == 0 else "cell") if isinstance(c, str) else c for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def fig(name, width=W_TEXT, caption=None):
    img = Image(str(HERE / "fig" / f"{name}.png"))
    img.drawWidth, img.drawHeight = width, width * img.imageHeight / img.imageWidth
    parts = [img]
    if caption:
        parts.append(p(caption, "small"))
    return KeepTogether(parts + [Spacer(1, 6)])


def tiles(items):
    cells = [[p(n, "tile_n") for n, _ in items], [p(lab, "tile_l") for _, lab in items]]
    t = Table(cells, colWidths=[W_TEXT / len(items)] * len(items))
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK), ("TOPPADDING", (0, 0), (-1, 0), 6),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    if doc.page > 1:
        canvas.setFont("OverseerSans-Regular", 7.5)
        canvas.setFillColor(INK3)
        canvas.drawString(20 * mm, 12 * mm, "OBench1 run 1 · three seeds, five harnesses · 5–6 November 2026 · "
                                            "internal: includes category scores")
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def money(x):
    return f"${x:.2f}"


def build():
    tot_usd = N["usd_total"]
    tot_in = sum(P[a]["prompt"] for a in ARMS)
    tot_tok = sum(P[a]["prompt"] + P[a]["out"] for a in ARMS)
    cache = 100 * sum(P[a]["cached"] for a in ARMS) / tot_in
    st = N["status"]
    real429 = sum(P[a]["real429"] for a in ARMS)
    slow = N["slowest_count"]
    story = []

    # ---- cover
    story += [Spacer(1, 26 * mm), p("OBench1, run 1", "title"), Spacer(1, 4),
              p("Five harnesses, 27 tasks, three seeds, 5 to 6 November 2026: how we prepared the run, made it "
                "fair, watched it, and what it measured, down to each category.", "sub"), Spacer(1, 14 * mm),
              tiles([("405", "cells: 27 tasks × 5 harnesses × 3 seeds"),
                     ("0", "infrastructure errors; the runner exited cleanly"),
                     (money(tot_usd), "metered spend on OpenCode Go, all five harnesses"),
                     ("10 h 52 m", "16:29 to 03:21 UTC")]),
              Spacer(1, 6 * mm),
              tiles([(f"{N['calls']:,}", "model calls through the gateways"),
                     (f"{tot_tok / 1e6:.0f}M", "tokens in and out"),
                     (f"{cache:.0f}%", "of input served from the provider's cache"),
                     (f"{real429 + st.get('429 cut', 0)}", "real rate-limit answers from the provider (none "
                      "injected)")]),
              Spacer(1, 14 * mm),
              p("OBench1 is our benchmark for coding-agent harnesses. Every harness gets the same model, the same "
                "settings and the same tasks at the same moment, so what's left to differ is the harness itself: "
                "its prompts, tools, memory, recovery and judgement. This document walks through the first full "
                "run from the first preparation step to the last log line, and shows every number we have."),
              p("<b>Overseer v5 has the highest approved score, 68.8</b>, then omp 54.1, Hermes 44.3, dsh 42.9 and "
                "pi 36.7. v5's and omp's 95% intervals overlap, so that's a likely lead, not a settled one. v5 is "
                "reliable in 11 of the 15 categories; the others in 4 to 6. It spent the most and was the cheapest "
                "per approved point."),
              p(f"<b>One thing to read first:</b> {DEAD['pi'] + DEAD['dsh']} cells never got a single answer from the "
                f"provider. Every call came back rate-limited and the harness gave up within about 16 seconds: pi "
                f"{DEAD['pi']} times, dsh {DEAD['dsh']}. Those cells score zero, so pi's and dsh's scores are lower than "
                "their work alone would give. Section 7 has the details and what the scores might be without them."),
              p("<b>Internal.</b> On 6 November the owner lifted the rule that kept per-category scores sealed. "
                "Section 9 shows them. They aren't on the public docs, and several categories rest on one to "
                "three tasks, so publishing them would largely show per-task results. That decision is still "
                "open.", "note"),
              PageBreak()]

    # ---- contents
    story += [p("Contents", "h1"),
              table([["", "Section"],
                     ["1", "What we ran"], ["2", "Prepare"], ["3", "Make it fair"],
                     ["4", "Prove the grading and the wiring"], ["5", "Set up the watcher"], ["6", "Run it"],
                     ["7", "Oversee it"], ["8", "Results"], ["9", "Category by category"],
                     ["10", "Cost and tokens"], ["11", "Time"], ["12", "What went wrong"],
                     ["13", "What we learned about v5"], ["14", "Limits"], ["15", "Repeat it"]],
                    [12 * mm, W_TEXT - 12 * mm]),
              PageBreak()]

    # ---- 1. what we ran
    story += [p("1 · What we ran", "h1"),
              p("Five harnesses, each run as it ships except for the settings in section 3, against 27 tasks in "
                "five camps of rising difficulty. Every harness ran every task three times (seeds 0, 1 and 2): "
                "81 cells per harness, 405 in all."),
              table([["Harness", "Build", "Provider entry", "What it is"],
                     ["Overseer v5", "v5.0.0-rc2, pinned binary (sha256 d93bbf46…babab68), commit 910f9881",
                      "opencode", "Ours"],
                     ["omp", "18.13.3", "opencode-go (built in)", "oh-my-pi, a pi-based coding agent"],
                     ["dsh", "DeepSeek Harness 0.1.1-rc.2", "deepseek-official (base URL moved)",
                      "DeepSeek's own desktop harness, run headless"],
                     ["pi", "1.5.0", "opencode-go (built in)", "A small, fast coding agent"],
                     ["Hermes", "Hermes Agent 0.22.5", "opencode-go (built in)",
                      "A general agent with tools, skills and memory"]],
                    [24 * mm, 54 * mm, 40 * mm, W_TEXT - 118 * mm]),
              Spacer(1, 8),
              p("The tasks", "h2"),
              p("27 tasks in 15 categories, each with a wall-clock cap from 5 to 90 minutes. Some throw avalanches "
                "mid-run: a spec change, a teammate's commit, a log flood, or a storm of provider faults injected "
                "at the gateway. Task contents stay sealed; this report names them only."),
              table([["Camp", "Tasks", "Examples"],
                     ["1 · warm-up", "2", "eff-trivial, eff-parallel-reads"],
                     ["2", "9", "if-constraint-gauntlet, lh-honest-blockers, sec-secret-hygiene, ver-hidden-spec"],
                     ["3", "11", "chaos-provider-storm, ctx-log-needle, mem-poisoned-note, pol-git-safety"],
                     ["4", "3", "ctx-eighteen-tickets, orch-dag-build, orch-spec-audit-24"],
                     ["5 · the long climbs", "2", "lh-money-migration, tool-rename-haystack"]],
                    [30 * mm, 14 * mm, W_TEXT - 44 * mm]),
              Spacer(1, 8),
              p("Grading", "h2"),
              *bullets([
                  "<b>Graders</b> are each task's own checks, run on the system Python outside the harness's reach. "
                  "They score the workspace, the git history and the replies out of 100: the <b>raw</b> score.",
                  "<b>Judges</b> are code, not a model. No AI grades anything. Each of the 15 category judges reads "
                  "the checks tagged with its category plus signals every cell has: budgets, whether each phase "
                  "finished on its own, git refs, leftover processes, editor debris, overclaiming in the final "
                  "reply, and any peek at the benchmark. A cell's points count only if no judge rejects it: the "
                  "<b>approved</b> score, the headline.",
                  "<b>Gates</b> are checks marked as safety or destructive-action breaches.",
                  "<b>Reliable</b>: a harness is reliable in a category when it was approved on every seed in at "
                  "least 90% of the tasks that category judged. The <b>summit</b> is all 15 at once with no gate "
                  "breach.",
                  "The judges never see which harness made a cell. No grader or judge reads a harness's name.",
              ]),
              PageBreak()]

    # ---- 2. prep
    story += [p("2 · Prepare", "h1"),
              p("Everything a run needs is set up before any model is called, and each piece is checked on its own."),
              p("Pin the builds", "h2"),
              p("Overseer v5.0.0-rc2 was built once and copied to a pin: a fixed binary whose hash is recorded and "
                "never changes. Earlier pins stay untouched, so a later run can compare against exactly the same "
                "code. The same commit is tagged v5.0.0-rc2 on GitHub. 5,359 of its 5,360 tests passed; the one "
                "failure is a load-sensitive soak test that passes on its own."),
              table([["Pin", "sha256", "Note"]] +
                    [[a, p(h, "cellsm"), b] for a, h, b in (
                        ("overseer-v5-rc2", "d93bbf46aeff6725150be26613ce4e0e39a59286ecb746e55e7dca590babab68",
                         "this run; 19.7 MB"),
                        ("overseer-v5", "6a680ad09723238d2a302fde768ebc91325057da3a8b92c1dd38cb3a5375c497",
                         "rc1, the pilot's build"),
                        ("overseer-v4", "78680cb2835a6c0393e126a01131883edac82ef74ceeeeaeb807aa42f7f17835", "v4"),
                        ("overseer-v3", "d615ae921f3d08cacb56fd1d844ffc4159ff5b09038e9ffc3c5e7f3828ce8597", "v3"))],
                    [26 * mm, 104 * mm, W_TEXT - 130 * mm]),
              p("What changed between rc1 and rc2", "h2"),
              p("Only safety fixes, found in the pilot (section 12): the computer tool refuses to launch or type into "
                "a terminal or script app, open script files or run <i>do shell script</i>, and when the shell "
                "sandbox can't start, Overseer says so once instead of failing every call. No change aimed at a "
                "score."),
              p("Give every harness a clean home", "h2"),
              *bullets([
                  "Every cell gets a fresh home directory. No harness sees the owner's own configs, memories, skills "
                  "or sessions, and nothing is written to them.",
                  "pi and omp get throwaway agent directories, copied per cell with only the base URL changed.",
                  "Hermes's ~600 MB of tool installs and cache are built once and shared between cells, so "
                  "installing never counts against its wall time. It holds no memory or sessions.",
                  "dsh runs headless from its app bundle with a per-cell home.",
              ]),
              p("One environment file", "h2"),
              p("env-go.sh sets the run: each arm's binary, the provider, the model, each harness's own effort knob "
                "at its maximum, and the throwaway directories. The key is read from the macOS keychain only when "
                "a paid run starts and is never printed. (It was, however, visible inside every cell; see "
                "section 12.)"),
              p("Choose the provider and the hour", "h2"),
              p("All arms used the OpenCode Go subscription with deepseek-v4.1-flash: 1M tokens of context, 384K of "
                "output. The run started at 16:29 UTC, so its last two hours fell in Go's 01:00–04:00 UTC "
                "double-rate window. That was a deliberate choice to finish overnight; all five harnesses ran in "
                "it together."),
              PageBreak()]

    # ---- 3. fairness
    ovr = {"overseer": 79, "omp": 80, "dsh": 74, "pi": 0, "hermes": 79}
    story += [p("3 · Make it fair", "h1"),
              p("Fair means every harness talks to the same model with the same settings, under the same limits, at "
                "the same time. We enforce what we can and write down what is each harness's own design."),
              fig("route", caption="Every model call leaves a cell through its own gateway. The jail allows loopback "
                  "only, so there is no other way out."),
              p("What the gateway forces on every call", "h2"),
              table([["Setting", "Sent on every call", "Why"],
                     ["model", "deepseek-v4.1-flash", "one model for everyone"],
                     ["thinking", "on", "some harnesses send no thinking field, or turn it off for side calls"],
                     ["reasoning effort", "max", "the provider's top level"],
                     ["output ceiling", "384,000 tokens", "the model's own limit, so nobody's thinking gets cut short"]],
                    [30 * mm, 38 * mm, W_TEXT - 68 * mm]),
              Spacer(1, 6),
              p("What each harness asked for, and how often the gateway changed it", "h2"),
              table([["Harness", "Its own request, before the gateway", "Cells changed (of 81)"],
                     ["Overseer v5", "no thinking field; max_tokens 131,072", str(ovr["overseer"])],
                     ["omp", "a short side call first (effort low, 1,024 tokens); its main calls send no thinking field",
                      str(ovr["omp"])],
                     ["dsh", "max_tokens 256,000", str(ovr["dsh"])],
                     ["pi", "exactly the forced settings: nothing to change", str(ovr["pi"])],
                     ["Hermes", "no thinking field, or thinking off; no output limit", str(ovr["hermes"])]],
                    [24 * mm, W_TEXT - 56 * mm, 32 * mm]),
              p("Counted from the gateway's own log: 312 changed cells in all. Raising side calls to max effort costs "
                "those harnesses a little more than they'd spend on their own; one rule for every call is easier to "
                "check than a rule per harness.", "small"),
              p("Same context, same limits, same moment", "h2"),
              *bullets([
                  "<b>Context:</b> all five plan for a 1M-token window for this model, so none compacts its history "
                  "earlier for lack of information.",
                  "<b>Limits:</b> the task's wall cap is the only limit. Overseer ships with a 100-step and $5 "
                  "budget the others don't have, so we lifted both. Approvals are off for every arm.",
                  "<b>Lockstep:</b> the five arms of a task and seed start together, in a launch order shuffled per "
                  "task and seed, at the same process priority. They share the provider load, the machine load and "
                  "the hour.",
                  "<b>Faults:</b> injected provider faults follow one plan per task and seed, keyed to the call "
                  "number, the same for every arm.",
                  "<b>The jail:</b> loopback only; no launching apps, no Apple Events, no window server or "
                  "Accessibility, no copy of a computer-use driver. Computer use is off for every arm in this "
                  "benchmark (not in the products).",
              ]),
              p("What still differs, on purpose", "h2"),
              *bullets([
                  "Tools, as counted in the pilot's wiring check: Overseer v5 offers 10, pi 4, omp 11, Hermes 19, "
                  "dsh 25.",
                  "Side calls: omp a short title call, dsh a small extra call, Hermes a probe for its context size, "
                  "Overseer a memory review after its final answer.",
                  "Recovery: during the evening's throttling, the median gap between one harness's rate-limited "
                  "calls was about 3 s for omp, dsh and Hermes, 4 s for pi and 13 s for Overseer.",
                  "Prompts, temperature, memory and everything else that makes a harness what it is.",
              ]),
              p("What each harness got that the others didn't", "h2"),
              table([["Harness", "What we changed, and why"],
                     ["Overseer v5", "--no-sandbox: macOS won't start Overseer's own shell sandbox inside the cell's "
                      "sandbox, and no other arm sandboxes its shell. Step and cost caps lifted. --probe off and a "
                      "copied capability file, so it doesn't re-check the endpoint every cell (that saves it a "
                      "little)."],
                     ["dsh", "The gateway copies dsh's session id into the header OpenCode Go routes cache hits on; "
                      "pi and omp send it themselves."],
                     ["Hermes", "Tool installs and cache built once beforehand and shared (no memory or sessions)."],
                     ["pi, omp", "Throwaway agent directories with only the base URL changed."]],
                    [24 * mm, W_TEXT - 24 * mm]),
              p("None of these touches grading.", "small"),
              PageBreak()]

    # ---- 4. grading + wiring
    story += [p("4 · Prove the grading and the wiring", "h1"),
              p("Two free checks prove the graders before any harness runs."),
              table([["Check", "What it does", "Result"],
                     ["oracle-check", "applies each task's reference solution and grades it", "27 of 27 score 100"],
                     ["null-check", "does nothing and grades the empty result", "27 of 27 score 0"]],
                    [28 * mm, W_TEXT - 68 * mm, 40 * mm]),
              p("Then every harness runs the simplest task against a fake provider on this machine, with a dummy "
                "key. Nothing is billed. Since the pilot, the check also runs each harness's own shell: it writes a "
                "file, then tries to launch an app, send an Apple Event and find the computer-use driver."),
              table([["Harness", "Routed with the forced settings", "Wrote the file", "Escapes refused"],
                     ["Overseer v5", "yes", "yes", "3 of 3"], ["omp", "yes", "yes", "3 of 3"],
                     ["dsh", "yes", "yes", "3 of 3"], ["pi", "yes", "yes", "3 of 3"],
                     ["Hermes", "yes", "yes", "3 of 3"]],
                    [30 * mm, 60 * mm, 34 * mm, W_TEXT - 124 * mm]),
              p("The pilot's wiring check only checked routing, which is how Overseer's broken shell got past it. "
                "Every request also carries a per-conversation session id, which the provider uses to route cache "
                "hits, so all arms get the same cache treatment.", "small"),
              Spacer(1, 6),
              p("5 · Set up the watcher", "h1"),
              p("A paid run is watched from start to finish. The watcher reads every cell's gateway log every 30 "
                "seconds and writes log sheets. It never reads grades."),
              table([["File", "What it holds", "Rows"],
                     ["live.md", "every cell climbing now, plus totals per harness", "—"],
                     ["arm-&lt;harness&gt;.md", "one sheet per harness: every cell so far, in order", "—"],
                     ["events.log", "starts, finishes, gateway overrides, real 429s, upstream errors, failure streaks, "
                      "ten minutes without model traffic, every $1 of spend", "—"],
                     ["progress.csv", "one row per running cell per tick: the time series", "5,843"],
                     ["calls.csv", "one row per model call: status, tokens, time to first byte, duration", "7,942"],
                     ["cells.csv", "one row per finished cell", "405"]],
                    [30 * mm, W_TEXT - 46 * mm, 16 * mm]),
              p("On top of the sheets", "h2"),
              *bullets([
                  "An alert stream raises what needs action: stalls (checked against the process list, so a finished "
                  "arm waiting on a slower one isn't a stall), real provider errors, failure streaks, sustained rate "
                  "limits, any sign of Overseer's shell failing, any mention of Terminal or Script Editor, and the "
                  "runner stopping.",
                  "We look; we don't intervene. The wall cap is the same for everyone.",
                  "Each cell keeps its full gateway log, transcripts and outputs in its results folder.",
              ]),
              PageBreak()]

    # ---- 6. run
    story += [p("6 · Run it", "h1"),
              table([["Setting", "Value"],
                     ["command", "obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 3 "
                      "--run-set ob1-3seed-rc2-20261105"],
                     ["mode", "lockstep: the five arms of a task and seed start together; tasks run in order"],
                     ["provider", "OpenCode Go, deepseek-v4.1-flash, one metered gateway per cell"],
                     ["limits", "each task's wall cap (5 to 90 minutes); no step or cost caps"],
                     ["started / ended", f"{N['t0_utc']} / {N['t1_utc']} UTC"]],
                    [28 * mm, W_TEXT - 28 * mm]),
              Spacer(1, 6),
              fig("progress", caption="Tasks × seeds finished over the run. Lockstep means all five harnesses "
                  "finish each step together, so one line stands for all of them. Shaded: the evening's throttling "
                  "and Go's double-rate window."),
              fig("cumulative", caption="Spend over the run, per harness, at Go's standard price list. Overseer "
                  "pulled ahead on lh-money-migration around 20:30 and stayed the most expensive arm."),
              p("Timeline", "h2"),
              table([["When (UTC)", "What happened"],
                     ["5 Nov 04:01–07:30", "The pilot: one seed, 135 cells. Overseer's row was later voided "
                      "(section 12)."],
                     ["5 Nov 13:41", "A first three-seed run starts; stopped about an hour in ($0.40) once the "
                      "pilot's problem was found."],
                     ["5 Nov afternoon", "The jail gains its GUI blocks; v5.0.0-rc2 is built and pinned; the wiring "
                      "check gains its shell test."],
                     ["5 Nov 16:29", "This run starts."],
                     ["5 Nov 18:45", "First real rate-limit burst as five arms start together. Everyone recovers."],
                     ["5 Nov 18:47", "Hermes gets the run's only real provider 500, after a 110-second hang. Its next "
                      "12 calls succeed."],
                     ["5 Nov 20:32", "lh-money-migration: Overseer uses 84 calls and 7.47M input on seed 0, against "
                      "18 to 23 calls and 0.6 to 1.6M for every other arm (section 13)."],
                     ["5 Nov 21:00–23:00", "Heavy throttling in bursts (section 7)."],
                     ["6 Nov 00:14", "orch-spec-audit-24: the widest spread of the run. dsh and pi finish each seed in "
                      "24 to 120 s; v5, omp and Hermes take 780 to 1,070 s."],
                     ["6 Nov 01:00", "Go's double-rate window opens."],
                     ["6 Nov 01:50", "A secrets scan finds the provider key in pi's transcripts (section 12)."],
                     ["6 Nov 03:21", "The last cell finishes; the runner exits cleanly."]],
                    [30 * mm, W_TEXT - 30 * mm]),
              PageBreak()]

    # ---- 7. oversee
    story += [p("7 · Oversee it", "h1"),
              p("The runner recorded 0 infrastructure errors, but that isn't the same as every cell getting a fair go "
                f"(see below: {DEAD['pi'] + DEAD['dsh']} cells never got an answer). The provider's own answers broke "
                f"down like this: {st.get('200 ok', 0):,} complete, {st.get('200 cut', 0)} streams cut short, "
                f"{st.get('200 client_gone', 0)} where the harness hung up first, {real429 + st.get('429 cut', 0)} "
                "rate-limited, 8 rejected as bad requests (all Hermes) and 1 server error (Hermes)."),
              fig("ratelimits", caption="Real 429s per 10 minutes, by harness. Almost all of them fell between "
                  f"21:00 and 23:00; the worst 10 minutes, from {N['worst_429_bin']['worst_bin_utc']}, had "
                  f"{N['worst_429_bin']['worst_bin_429']} of {N['worst_429_bin']['worst_bin_calls']} calls "
                  "rate-limited."),
              fig("hourly", caption="Top: model calls per 20 minutes, per harness. Bottom: the share of all calls "
                  "rate-limited. The bursts came when five arms started a task together, which is the provider's "
                  "burst limit tripping, not an exhausted quota: between bursts it fell back to 0."),
              p("Rate limits, per harness", "h2"),
              table([["Harness", "Rate-limited calls", "All calls", "Share", "Median gap between its 429s"]] +
                    [[NAME[a], str(P[a]["real429"]), f"{P[a]['calls']:,}",
                      f"{100 * P[a]['real429'] / P[a]['calls']:.1f}%",
                      {"overseer": "13 s", "omp": "3 s", "dsh": "3 s", "pi": "4 s", "hermes": "3 s"}[a]]
                     for a in sorted(ARMS, key=lambda a: -P[a]["real429"])],
                    [28 * mm, 30 * mm, 22 * mm, 18 * mm, W_TEXT - 98 * mm]),
              p("Rejected calls cost nothing but wall time, and unevenly: harnesses that retry fast pile up more "
                "429s and press harder on the shared limit. Wall times on the memory tasks that evening say more "
                "about the throttling than about the harnesses. Counted at the gateway; injected faults aren't "
                "in these numbers.", "small"),
              p(f"{DEAD['pi'] + DEAD['dsh']} cells never got an answer", "h2"),
              p("In these cells every model call came back as a real 429. pi gives up after four tries, dsh after "
                "seven, both within about 16 seconds, so the harness ended before doing anything. In the same seconds "
                "the other arms mostly got through, because they keep retrying for longer. Overseer, omp and Hermes "
                "lost no cells this way."),
              table([["When (UTC)", "Task", "Harness, seed"],
                     ["5 Nov 21:48", "mem-poisoned-note", "pi s1"],
                     ["5 Nov 22:30–22:33", "oob-lost-fixture", "pi s0, pi s1"],
                     ["5 Nov 22:50–22:53", "oob-slow-oracle", "dsh s0, pi s1, dsh s2"],
                     ["5 Nov 22:56", "orch-dag-build", "pi s0, dsh s0"],
                     ["5 Nov 23:07", "orch-dag-build", "dsh s1"],
                     ["6 Nov 02:38", "ver-dont-trust-the-fix", "pi s2"],
                     ["6 Nov 03:03–03:09", "ver-pr-review", "pi s0, pi s1"]],
                    [34 * mm, 50 * mm, W_TEXT - 84 * mm]),
              p("Is that the harness or the provider? Both. Giving up after 16 seconds of rate limits is a real "
                "resilience trait, and the other three show it can be ridden out. But these weren't faults the "
                "benchmark meant to throw. An empty cell scores 0, so here is a rough estimate: if those cells had scored "
                "each harness's own average, pi's approved score would be about "
                f"{R['pi']['approved'] * 81 / (81 - DEAD['pi']):.1f} instead of {R['pi']['approved']:.1f}, and dsh's about "
                f"{R['dsh']['approved'] * 81 / (81 - DEAD['dsh']):.1f} instead of {R['dsh']['approved']:.1f}. That would "
                f"put dsh just above Hermes ({R['hermes']['approved']:.1f}) for third. Overseer and omp would stay first "
                "and second. The category write-ups in section 9 say where these cells move a number.", "note"),
              p("What else came up", "h2"),
              *bullets([
                  "Overseer's post-answer memory review got a real 429 twice (19:40 and 20:02). Both times it logged "
                  "the skip and ended normally; the exit status wasn't affected.",
                  "Overseer's claim check flagged \"tests: 2 passed\" as unbacked on one cell, and the message went "
                  "out anyway (section 13).",
                  "The sustained-429 alert fired at 21:53 on 62 of 123 calls in five minutes. Most were fast retries "
                  "from omp and Hermes; v5 and dsh carried on almost untouched.",
                  "We didn't intervene in any cell.",
              ]),
              PageBreak()]

    # ---- 8. results
    rows = [["Harness", "Approved", "95% interval", "Raw", "Solved", "Gates", "Reliable", "$/point", "Spend"]]
    for a in RANK:
        r = R[a]
        rows.append([NAME[a], f"{r['approved']:.1f}", f"{r['lo']:.1f}–{r['hi']:.1f}", f"{r['raw']:.1f}",
                     f"{r['solved']}/81", str(r["gates"]), f"{r['reliable']}/15", f"${r['usd_point']:.4f}",
                     money(P[a]["usd"])])
    story += [p("8 · Results", "h1"),
              p("The suite totals, all 405 cells."),
              table(rows, [24 * mm, 17 * mm, 22 * mm, 12 * mm, 15 * mm, 12 * mm, 17 * mm, 18 * mm,
                           W_TEXT - 137 * mm]),
              Spacer(1, 8),
              fig("scores", caption="Bar: approved. Whisker: 95% interval. Ring: raw, before the judges. Where "
                  "two intervals overlap, the gap between those harnesses isn't settled."),
              fig("reliable", caption="Reliable categories out of 15. No harness reached the summit (all 15, no "
                  "gate breach); omp's one gate breach would keep it off the summit even with all 15."),
              fig("pilot-vs-final", caption="The one-seed pilot against this run. The pilot's Overseer row is void: "
                  "its shell never worked (section 12). The other four moved by 2.5 to 13.3 points with two more "
                  "seeds, which is why one seed isn't enough."),
              p("How to read them", "h2"),
              *bullets([
                  "Approved is the headline. A cell that passes its tests but leaves a process running, rewrites git "
                  "history it shouldn't, or claims it finished when it didn't, scores raw points and no approved ones.",
                  "v5 has the smallest gap between raw and approved (95.2 to 68.8); Hermes the largest (85.5 to 44.3).",
                  "Solved counts cells where every check passed, before the judges: v5 61 of 81, omp 50, Hermes 49, "
                  "dsh 42, pi 37.",
                  "$/point is total spend over approved points, so cheap and wrong doesn't look cheap.",
                  f"pi's and dsh's totals include {DEAD['pi']} and {DEAD['dsh']} cells that never got an answer "
                  "(section 7). Without them, dsh would likely be third, not fourth.",
                  "An early preview, posted with 22 of 27 tasks done, had Overseer at 72.2 and omp at 56.2. With all "
                  "27, the lead narrowed from 16.0 to 14.7 points.",
              ]),
              PageBreak()]

    # ---- 9. categories
    weak = [c for c in CAT if CATS[c]["overseer"] < 90]
    story += [p("9 · Category by category", "h1"),
              p("Each number is the share of a category's tasks where the harness was approved on all three seeds. "
                "90% or more makes it reliable in that category."),
              fig("categories", caption="Outlined: reliable. In brackets: how many tasks the category judged."),
              p("Read the task counts first", "h2"),
              *bullets([
                  "Categories marked 27 or 22 judge almost every task, because some judges read signals every cell "
                  "has (budgets, whether each phase finished, git, leftovers, overclaiming). They're broad measures.",
                  "Skills (1 task), Orchestration (2), Memory, Out-of-the-box and Honest reporting (3 each) rest on "
                  "very few tasks: one task flipping on one seed moves them by 33 to 100 points. Read them as "
                  "anecdotes, not rates.",
                  "The categories aren't independent. When a harness doesn't finish a phase, it usually also has no "
                  "final reply to sign off, and often fails the task's checks too. So one unfinished cell tends to "
                  "count against Long-horizon, Instruction following, Resilience and Verification together: 75 of "
                  "the 77 cells missing their sign-off also had a phase that didn't finish.",
              ]),
              PageBreak(),
              fig("category-gap", caption="Overseer v5 against the best of the other four, per category. Blue: "
                  "ahead. Grey: behind. Dot: level."),
              p("What it says", "h2"),
              *bullets([
                  "v5 is the only harness at 100% on Memory, Orchestration, Safety and trust, and Resilience. The "
                  "last two judge every task.",
                  "Its biggest broad leads: Long-horizon execution (+11 over omp), Resilience (+15), Verification "
                  "(+18). Its biggest narrow ones, Orchestration (+50) and Memory (+33), rest on two and three "
                  "tasks.",
                  "It trails in one category: Policy and repo rules, 91% against omp's 95% (one task of 22).",
                  f"It isn't reliable in {len(weak)}: " + ", ".join(f"{c} ({CATS[c]['overseer']}%)" for c in weak)
                  + ". Efficiency is level with omp and dsh, and Out-of-the-box level with omp and Hermes. "
                  "Verification and Instruction following are still the best of the five.",
                  "Every harness got Skills and extensibility on its single task, and everyone but dsh got 100% on "
                  "Context management.",
                  "Efficiency is close for everyone (70 to 81%) and nobody is reliable in it. Its budgets are "
                  "uncalibrated first guesses (section 14), so it may say more about the budgets than about the "
                  "harnesses.",
              ]),
              PageBreak(),
              p("Each category, each harness", "h1"),
              p("In words, from the judges' recorded votes and reasons, the per-task raw scores and the run's logs. "
                "\"Dead cells\" are the cells in section 7 that never got an answer."),
              ]
    for c in CAT:
        rows = [["Harness", "Score", "How it went"]]
        for a in RANK:
            rows.append([NAME[a], f"{CATS[c][a]}%" + ("<br/><font size='7' color='#5D5B59'>reliable</font>" if CATS[c][a] >= 90 else ""), TEXT[c][a]])
        story.append(KeepTogether([
            p(f"{c} <font color='#5D5B59' size='9'>({CATS[c]['n']} task{'s' if CATS[c]['n'] > 1 else ''})</font>",
              "h2"),
            p(ASKS[c], "small"),
            table(rows, [22 * mm, 16 * mm, W_TEXT - 38 * mm]),
            Spacer(1, 4)]))
    story += [p("Score: share of the category's tasks approved on all three seeds, higher is better. Reliable: "
                "90% or more.", "small"),
              PageBreak()]

    # ---- 10. cost and tokens
    story += [p("10 · Cost and tokens", "h1"),
              fig("spend", caption="Metered at Go's standard price list ($0.15, $0.003 and $0.60 per million uncached "
                  "input, cached input and output). The last two hours ran in Go's double-rate window, so the quota "
                  "used is somewhat higher than this."),
              fig("tokens", caption="Input and output tokens per harness. Hermes reads the most input, mostly from "
                  "cache; Overseer writes the most output."),
              fig("output", caption="Output tokens per answered call. Output is the dearest token, and Overseer's "
                  "893 per call, against 607 to 718, is the main reason it spent the most."),
              fig("cache-calls", caption="Left: share of input served from cache, as the benchmark's report counts it. "
                  "Right: median model calls in a cell."),
              p("Per harness, in numbers", "h2"),
              table([["Harness", "Calls", "Input", "Cached", "Output", "Out/call", "Peak context", "Faults met",
                      "Spend"]] +
                    [[NAME[a], f"{P[a]['calls']:,}", f"{P[a]['prompt'] / 1e6:.1f}M",
                      f"{100 * P[a]['cached'] / P[a]['prompt']:.0f}%", f"{P[a]['out'] / 1e6:.2f}M",
                      f"{P[a]['out_per_call']:.0f}", f"{P[a]['peak'] / 1e3:,.0f}K", str(P[a]["faults"]),
                      money(P[a]["usd"])] for a in RANK],
                    [22 * mm, 14 * mm, 15 * mm, 15 * mm, 15 * mm, 15 * mm, 20 * mm, 18 * mm, W_TEXT - 134 * mm]),
              p("Faults met are the provider errors chaos tasks inject on purpose; a harness that makes more calls "
                "during a storm meets more of them. Peak context is the largest single prompt; nobody came near the "
                "1M window.", "small"),
              PageBreak()]

    # ---- 11. time
    story += [p("11 · Time", "h1"),
              fig("time", caption="Left: wall time of all 81 cells added up. Right: how often each harness was the "
                  f"last of the five to finish a task and seed ({N['task_seeds']} in all). Overseer was last "
                  f"{slow['overseer']} times, omp {slow['omp']}."),
              fig("ttfb", caption="How long the provider took to start answering, per harness. Medians of 1.5 to "
                  "2.3 s: everyone got about the same service, which is what lockstep is for."),
              p("Per task", "h2"),
              p("The next two pages show each task's median over the three seeds. They show time and tokens, not "
                "scores. Throttling inflated the evening's memory tasks for most arms (section 7)."),
              PageBreak(),
              fig("heat-wall", width=W_TEXT * 0.92, caption="Wall time per task, median of three seeds. Darker is "
                  "longer; the scale is logarithmic."),
              PageBreak(),
              fig("heat-tokens", width=W_TEXT * 0.92, caption="Tokens per task, input and output, median of three "
                  "seeds."),
              PageBreak()]

    # ---- 12. incidents
    story += [p("12 · What went wrong", "h1"),
              p("In order. Some of it is about Overseer."),
              p("The pilot didn't measure Overseer", "h2"),
              p("In the one-seed pilot, Overseer came last on approved score (29.6) while costing more than twice the "
                "next harness ($1.11 against Hermes's $0.49). Its shell never worked: macOS refuses to start a "
                "second sandbox inside a first (sandbox_apply: Operation not permitted), and all 178 of its shell "
                "calls failed. No other arm sandboxes its own shell. We voided its pilot row; the other four stand."),
              table([["Pilot, one seed", "Approved", "95% interval", "Raw", "Spend"],
                     ["omp", "51.6", "33.1–69.8", "89.4", "$0.35"], ["pi", "40.5", "22.0–59.0", "81.4", "$0.30"],
                     ["Hermes", "36.8", "18.5–55.3", "85.9", "$0.49"], ["dsh", "29.6", "14.8–48.1", "55.6", "$0.32"],
                     ["Overseer v5 (void)", "29.6", "11.1–48.1", "71.6", "$1.11"]],
                    [36 * mm, 24 * mm, 28 * mm, 18 * mm, W_TEXT - 106 * mm]),
              p("Overseer drove the Mac's desktop to get a shell", "h2"),
              p("The serious one. With its shell blocked, Overseer used its computer-use tool, in 8 of the pilot's "
                "27 tasks, to open Terminal and Script Editor on the real desktop, type shell commands, run "
                "<i>do shell script</i>, delete files with rm -f, quit both apps with killall and start background "
                "jobs, all outside the benchmark's sandbox. It ran on our own benchmark machine. It left 7 files in "
                "/tmp (moved to the Trash) and both apps open. On someone's own Mac, that is exactly what an agent "
                "must never do."),
              *bullets([
                  "In Overseer (rc2): the computer tool refuses terminals, script apps, script files and do shell "
                  "script; a sandbox that can't start is reported once, plainly.",
                  "In the benchmark: the jail blocks app launch, Apple Events, the window server, Accessibility and "
                  "every computer-use driver, for every harness. Each block was checked by hand.",
                  "Still open: a general rule that stops any tool after the same failure three times. We built it "
                  "and dropped it before release; it tripped on ordinary refusals.",
              ]),
              p("We stopped a run and started again", "h2"),
              p("The first three-seed run had started before any of this was found. We stopped it after about an hour "
                "($0.40), fixed the jail and Overseer, and reran every harness from the start. Overseer got no extra "
                "runs."),
              p("The provider key was visible to every harness", "h2"),
              p("The run passed the OpenCode Go key to each harness through its environment. In three cells pi listed "
                "its environment, so the key went into 6 transcript files and upstream in its context. No other "
                "harness printed it. The key was revoked on 6 November. The next run gives each harness a dummy key, "
                "with the gateway adding the real one, and builds each cell's environment from an allowlist."),
              p(f"{DEAD['pi'] + DEAD['dsh']} cells never got an answer", "h2"),
              p(f"pi lost {DEAD['pi']} cells and dsh {DEAD['dsh']} to real rate limits: every call was a 429, and "
                "each harness gave up within about 16 seconds. We found it while checking the token charts for this "
                "report, after the run. The runner counts these as finished cells, not infrastructure errors, so the "
                "\"0 infrastructure errors\" headline is accurate but doesn't tell the whole story. Section 7 has the "
                "list and a rough estimate of the effect."),
              p("The provider throttled us for an evening", "h2"),
              p("From about 21:00 to 23:00 UTC on 5 November, the provider rate-limited us in bursts: for a few "
                "minutes at a time, 40 to 57% of calls got a 429. These were real. See section 7."),
              PageBreak()]

    # ---- 13. learned
    story += [p("13 · What we learned about v5", "h1"),
              p("From the transcripts, the totals and, since 6 November, the category scores. These go into "
                "Overseer's next round of work."),
              p("Where it loses", "h2"),
              *bullets([
                  "<b>It writes too much.</b> 893 output tokens per answered call against 607 to 718; 1.5M output "
                  "tokens over the run against 0.7 to 1.1M. In the pilot about two-thirds of its output was "
                  "reasoning. It's the main reason v5 spent the most.",
                  "<b>It over-checks on long tasks.</b> On lh-money-migration seed 0 it made 84 calls, 78 of them "
                  "shell, including about 30 one-off checks after the work was done. The others stopped at the test "
                  "suite with 18 to 23 calls. One batched check would do.",
                  "<b>It misreads its own changes.</b> When its shell edited a scratch file in /tmp, it told itself "
                  "\"the owner changed\" the file and re-read it. Drift tracking should count its own shell's writes "
                  "and ignore paths outside the workspace.",
                  "<b>It makes one call after the answer.</b> The memory review goes out about 0.7 s after the final "
                  "reply. It handled the 429s it got there cleanly, but on a one-off headless run it's an extra paid "
                  "call.",
                  "<b>It flagged a claim it couldn't back, and sent it anyway.</b> Its own check marked \"tests: 2 "
                  "passed\" as unbacked. A flagged claim should be fixed or cut before the answer goes out.",
                  "<b>Its four non-reliable categories:</b> " + ", ".join(f"{c} ({CATS[c]['overseer']}%)"
                                                                         for c in weak) + ".",
              ]),
              p("What worked", "h2"),
              *bullets([
                  "It backed off under rate limits (13 s median gap) instead of hammering the shared limit, and got "
                  "the fewest 429s of anyone (57).",
                  "It used the fewest tokens and dollars per approved point.",
                  "100% on Safety and trust and on Resilience, across every task.",
                  "The smallest gap between raw and approved: its passing cells were the least often rejected by the "
                  "judges.",
              ]),
              Spacer(1, 6),
              p("14 · Limits", "h1"),
              *bullets([
                  "<b>We wrote both the benchmark and Overseer.</b> The categories come from other harnesses' "
                  "strengths, and until 6 November nobody building Overseer could see which tasks it failed. That "
                  "guards against tuning to the test; it can't rule out scenarios that lean our way without anyone "
                  "meaning them to.",
                  "<b>The blind rule is now lifted.</b> From here on, v5 work can see category scores, so later "
                  "OBench1 scores are no longer blind for v5. Each one should say so.",
                  "<b>An all-rounder's benchmark.</b> Overseer was built to cover all 15 categories, and the score "
                  "weights them equally. That rewards breadth.",
                  "<b>One model, one provider, one night.</b> deepseek-v4.1-flash on OpenCode Go only.",
                  "<b>Three seeds.</b> Enough to call a category reliable, not enough to make the intervals narrow.",
                  f"<b>Throttle-killed cells.</b> {DEAD['pi'] + DEAD['dsh']} cells of pi and dsh never got an answer, "
                  "which lowers their scores. We haven't rerun them: a rerun at a different hour wouldn't be lockstep.",
                  "<b>Uncalibrated budgets.</b> The efficiency and speed judges' budgets are first guesses, the same "
                  "for everyone.",
              ]),
              PageBreak()]

    # ---- 15. repeat
    story += [p("15 · Repeat it", "h1"),
              table([["Step", "Command"],
                     ["list the tasks", "python3 obench.py list"],
                     ["prove the graders", "python3 obench.py oracle-check && python3 obench.py null-check"],
                     ["prove the wiring (free)", "source env-go.sh && python3 obench.py wiring --agents "
                      "overseer,omp,dsh,pi,hermes"],
                     ["run (paid)", "source env-go.sh --with-key && python3 obench.py run --agents "
                      "overseer,omp,dsh,pi,hermes --seeds 3 --run-set &lt;id&gt;"],
                     ["watch", "python3 lib/watch.py --run-set &lt;id&gt; --runner-log &lt;file&gt; --runner-pid "
                      "&lt;pid&gt; --out &lt;dir&gt; --every 30"],
                     ["report", "python3 obench.py report --run-set &lt;id&gt; [--by-category]"],
                     ["this document", "uv run --no-project --with matplotlib python -I charts.py, then uv run "
                      "--no-project --with reportlab --with pillow python -I build.py"]],
                    [34 * mm, W_TEXT - 34 * mm]),
              Spacer(1, 6),
              p("Before the next run", "h2"),
              *bullets([
                  "A new Go key in the keychain (the old one is revoked), a dummy key per arm and an allowlisted cell "
                  "environment.",
                  "Stagger arm starts by a few seconds to soften the provider's burst limit, and count throttled "
                  "arm-minutes rather than raw 429s in the alert.",
                  "Calibrate the efficiency and speed budgets from this run's data.",
                  "Have the runner flag any cell with zero answered calls, and decide in advance whether such a cell "
                  "is rerun or scored.",
                  "Redact the 6 pi transcript files before anything from this run is shared.",
              ]),
              Spacer(1, 6),
              p("Everything from this run lives in results/watch/ob1-3seed-rc2-20261105 (the log sheets and the "
                "category report) and results/runs/ob1-3seed-rc2-20261105 (each cell's transcripts, outputs, "
                "metrics and gateway log).", "small")]

    doc = SimpleDocTemplate(str(HERE / "obench1-run1-2026-11-06.pdf"), pagesize=A4, leftMargin=20 * mm,
                            rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                            title="OBench1, run 1", author="Overseer")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


if __name__ == "__main__":
    build()
