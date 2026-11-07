"""The 2026-11-05 OBench1 pilot report: how the run was prepared, made fair, watched, and what it measured.

    uv run --no-project --with matplotlib python -I charts.py
    uv run --no-project --with reportlab python -I build.py

Writes obench1-pilot-2026-11-05.pdf next to this file. Type and colour follow
overseer-site/design-language (light mode: the grey page, the dark ink; Overseer Display and Sans).
"""

import json
from pathlib import Path

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = Path(__file__).resolve().parent
FONTS = Path.home() / "Desktop/overseer-hq/overseer-desktop/apps/desktop/assets/fonts"
for name in ("OverseerDisplay-Light", "OverseerDisplay-Regular", "OverseerSans-Light", "OverseerSans-Regular",
             "OverseerSans-Medium"):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / f"{name}.ttf")))

PAGE, INK = colors.HexColor("#D4D2CF"), colors.HexColor("#171615")
INK2, INK3, RULE = colors.HexColor("#5D5B59"), colors.HexColor("#8E8C8A"), colors.HexColor("#B9B7B4")
ARMS = ["overseer", "omp", "dsh", "pi", "hermes"]
NAME = {"overseer": "Overseer v5", "omp": "omp", "dsh": "dsh", "pi": "pi", "hermes": "Hermes"}
N = json.loads((HERE / "numbers.json").read_text())
P, R = N["per_arm"], N["report"]
W_TEXT = A4[0] - 40 * mm

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
    "cellh": ParagraphStyle("cellh", fontName="OverseerSans-Medium", fontSize=8, leading=10.5, textColor=INK),
    "tile_n": ParagraphStyle("tile_n", fontName="OverseerDisplay-Light", fontSize=22, leading=25, textColor=INK),
    "tile_l": ParagraphStyle("tile_l", fontName="OverseerSans-Regular", fontSize=8, leading=10.5, textColor=INK2),
    "bullet": ParagraphStyle("bullet", fontName="OverseerSans-Regular", fontSize=9.4, leading=13.6, textColor=INK,
                             leftIndent=11, bulletIndent=0, spaceAfter=3),
}


def p(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


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
    from PIL import Image as PILImage  # noqa: F401  (reportlab reads the size itself)
    img = Image(str(HERE / "fig" / f"{name}.png"))
    img.drawWidth, img.drawHeight = width, width * img.imageHeight / img.imageWidth
    parts = [img]
    if caption:
        parts.append(p(caption, "small"))
    return KeepTogether(parts + [Spacer(1, 6)])


def tiles(items):
    cells = [[p(n, "tile_n") for n, _ in items], [p(lab, "tile_l") for _, lab in items]]
    t = Table(cells, colWidths=[W_TEXT / len(items)] * len(items))
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
                           ("TOPPADDING", (0, 0), (-1, 0), 6)]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    if doc.page > 1:
        canvas.setFont("OverseerSans-Regular", 7.5)
        canvas.setFillColor(INK3)
        canvas.drawString(20 * mm, 12 * mm, "OBench1 field run · five-harness pilot · 5 November 2026")
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def money(x):
    return f"${x:.2f}"


def build():
    tot_usd = sum(P[a]["usd"] for a in ARMS)
    tot_calls = sum(P[a]["calls"] for a in ARMS)
    tot_tok = sum(P[a]["prompt"] + P[a]["out"] for a in ARMS)
    story = []

    # ---- cover
    story += [Spacer(1, 30 * mm), p("OBench1 field run", "title"), Spacer(1, 4),
              p("The five-harness pilot, 5 November 2026: how we prepared it, made it fair, watched it and what "
                "it measured.", "sub"), Spacer(1, 16 * mm),
              tiles([("135", "cells: 27 tasks × 5 harnesses, one seed"), ("0", "failed cells, infra errors or real "
                     "provider errors"), (money(tot_usd), "metered spend on OpenCode Go"),
                     ("3 h 29 m", "from the first call at 04:01 UTC to the last")]),
              Spacer(1, 6 * mm),
              tiles([(f"{tot_calls:,}", "model calls metered (3,020 answered; the rest were faults tasks injected)"), (f"{tot_tok / 1e6:.0f}M", "tokens in and "
                     "out across all arms"), ("93%", "of input tokens served from the provider's cache"),
                     ("1:1", "model, thinking, effort and output ceiling on every call")]),
              Spacer(1, 16 * mm),
              p("OBench1 is a benchmark for coding-agent harnesses. Every harness gets the same model, the same "
                "settings and the same tasks at the same moment, so the only thing left to differ is the harness "
                "itself: its prompts, tools, memory, recovery and judgement. This document walks through one full "
                "run from the first preparation step to the last log line. It's written so anyone can repeat it, "
                "and so anyone can check that it was fair."),
              p("This was a pilot: one seed. It proves the machinery and gives real costs. The scores in section 9 "
                "are a first read, not a verdict; their 95% intervals overlap, and the benchmark needs three seeds "
                "before it calls anything reliable."),
              PageBreak()]

    # ---- 1. what we ran
    story += [p("1 · What we ran", "h1"),
              p("Five harnesses, each run as it ships except for the three settings in section 3, against 27 tasks "
                "in five camps of rising difficulty. Every harness ran every task once (seed 0). Sections 2 to 8 are the steps of the run, in the order we took them."),
              table([["Harness", "Build", "Provider entry it uses", "What it is"],
                     ["Overseer v5", "pinned binary, sha256 6a680ad0… (ov5/integrate db1f6023)", "opencode",
                      "Our harness. The arm under test."],
                     ["omp", "18.13.3", "opencode-go (built in)", "oh-my-pi, a pi-based coding agent"],
                     ["dsh", "DeepSeek Harness 0.1.1-rc.2", "deepseek-official (base URL moved)",
                      "DeepSeek's own desktop harness, run headless"],
                     ["pi", "1.5.0", "opencode-go (built in)", "A small, fast coding agent"],
                     ["Hermes", "Hermes Agent 0.22.5", "opencode-go (built in)", "A general agent with tools, "
                      "skills and memory"]],
                    [24 * mm, 52 * mm, 42 * mm, W_TEXT - 118 * mm]),
              Spacer(1, 8),
              p("The tasks", "h2"),
              p("27 tasks across 15 categories, each with a wall-clock cap from 5 to 90 minutes. Camp 1 is the "
                "warm-up (two tasks), camp 5 the long climbs (two tasks that can run to millions of tokens). Some "
                "tasks throw avalanches mid-run: spec changes, a teammate's commit, log floods, or provider fault "
                "storms injected at the gateway. Task contents stay sealed; this report names them only."),
              table([["Camp", "Tasks", "Examples"],
                     ["1", "2", "eff-trivial, eff-parallel-reads"],
                     ["2", "9", "if-constraint-gauntlet, lh-honest-blockers, sec-secret-hygiene, ver-hidden-spec"],
                     ["3", "11", "chaos-provider-storm, ctx-log-needle, mem-poisoned-note, pol-git-safety"],
                     ["4", "3", "ctx-eighteen-tickets, orch-dag-build, orch-spec-audit-24"],
                     ["5", "2", "lh-money-migration, tool-rename-haystack"]],
                    [16 * mm, 16 * mm, W_TEXT - 32 * mm]),
              Spacer(1, 8),
              p("Grading", "h2"),
              p("Each task's own graders score the result out of 100 (the raw score). Then a panel of 15 category "
                "judges reads the evidence. A cell's points count only if no judge rejects it: that's the approved "
                "score, the headline number. Safety and destructive-action breaches are gates: one breach anywhere "
                "and that harness can't reach the summit. Which task or check failed stays sealed, so nobody can "
                "tune a harness to the test."),
              PageBreak()]

    # ---- 2. prep
    story += [p("2 · Prepare", "h1"),
              p("Everything a run needs is set up before any model is called, and each piece is checked on its own."),
              p("Pin the builds", "h2"),
              p("Overseer v5 was built once from the tip of its branch and copied to a pin, a fixed binary that "
                "never changes once recorded. Earlier pins stay untouched, so any later run can compare against "
                "exactly the same code."),
              table([["Pin", "sha256", "Source"],
                     ["overseer-v5", "6a680ad09723238d2a302fde768ebc91325057da3a8b92c1dd38cb3a5375c497",
                      "ov5/integrate db1f6023, release build, 19.7 MB"],
                     ["overseer-v4", "78680cb2835a6c0393e126a01131883edac82ef74ceeeeaeb807aa42f7f17835", "v4 pin"],
                     ["overseer-v3", "d615ae921f3d08cacb56fd1d844ffc4159ff5b09038e9ffc3c5e7f3828ce8597", "v3 pin"]],
                    [22 * mm, 100 * mm, W_TEXT - 122 * mm]),
              p("The same commit was pushed and tagged v5.0.0-rc1 the same night, so the binary under test is "
                "exactly what's on GitHub.", "small"),
              p("Give every harness a clean home", "h2"),
              *bullets([
                  "Every cell gets a fresh home directory. No harness sees the owner's own configs, memories, skills "
                  "or sessions, and nothing is ever written to them.",
                  "pi and omp get throwaway agent directories, copied per cell with only the base URL changed.",
                  "Hermes needs about 600 MB of tool environments and cache on first run. We built that once into a "
                  "shared folder (354 MB of tools, 244 MB of cache) and link it into each cell's home. It holds no "
                  "memory or sessions, so sharing it can't leak anything between cells. Hermes's own install in the "
                  "owner's home was confirmed untouched afterwards.",
                  "dsh runs headless from its app bundle with a per-cell home.",
              ]),
              p("One environment file", "h2"),
              p("A single file, env-go.sh, sets the run: which binary each arm uses, the provider, the model, every "
                "harness's own effort knob at its maximum, and the throwaway directories. The key is read from the "
                "macOS keychain only when a paid run starts and is never printed or written down."),
              p("Choose the provider", "h2"),
              p("All arms used the OpenCode Go subscription with deepseek-v4.1-flash: 1M tokens of context and "
                "384K of output, the same model the pay-as-you-go route serves at twice the price. (OpenCode's "
                "separate free model is a different, 200K-context variant; we didn't use it.) Go doubles its usage "
                "rate on weekdays 01:00–04:00 and 06:00–10:00 UTC, so the run was scheduled for 04:01 UTC."),
              p("Make room", "h2"),
              p("The machine had 42 GB free. About 78 GB of rebuildable build caches went to the Trash first, "
                "bringing it to about 120 GB; anything belonging to other projects was left alone. The run itself "
                "used under 1 GB, because each cell's workspace is removed when it finishes."),
              PageBreak()]

    # ---- 3. fairness
    story += [p("3 · Make it fair", "h1"),
              p("Fair means every harness talks to the same model with the same settings, under the same limits, "
                "at the same time. We enforce the parts we can, and write down the parts that are the harnesses' "
                "own design."),
              fig("route", caption="Every model call leaves a cell through its own gateway. The jail allows "
                  "loopback only, so there is no other way out."),
              p("What the gateway forces on every call", "h2"),
              p("Whatever a harness asks for, the call that reaches the provider carries these four settings. The "
                "gateway logs every time it had to change a request, so the overrides are on the record."),
              table([["Setting", "Sent on every call", "Why"],
                     ["model", "deepseek-v4.1-flash", "one model for everyone"],
                     ["thinking", "enabled", "some harnesses send no thinking field, or turn it off for side calls"],
                     ["reasoning_effort", "max", "the provider's top level (low, high and max were all checked)"],
                     ["output ceiling", "384,000 tokens", "the model's own limit, so no harness cuts its thinking short"]],
                    [32 * mm, 40 * mm, W_TEXT - 72 * mm]),
              Spacer(1, 6),
              p("What each harness asked for (first call of each cell)", "h2"),
              table([["Harness", "What it sent before the gateway", "Cells"],
                     ["Overseer v5", "no thinking field; max_tokens 131,072", "27"],
                     ["omp", "a short side call first: effort low, 1,024 tokens; its main calls send no thinking field",
                      "25"],
                     ["dsh", "max_tokens 256,000 (once: thinking off for a 64-token side call)", "24"],
                     ["pi", "exactly the forced settings: no change needed", "0"],
                     ["Hermes", "no thinking field, or thinking off; no output limit", "26"]],
                    [24 * mm, W_TEXT - 40 * mm, 16 * mm]),
              p("Raising side calls to max effort costs those harnesses a little more than they'd spend on their "
                "own. We accept that: one rule for every call is easier to verify than a rule per harness.", "small"),
              p("Same context window", "h2"),
              p("A harness decides when to compact its history from the context size it believes it has. We checked "
                "each one's own lookup for this model: all five plan for 1M tokens. Overseer v5's profile says "
                "1M / 384K, pi's and omp's Go catalogs say 1M / 384K, dsh falls back to its 1M default, and Hermes "
                "resolves 1M even with the network blocked, as it is inside the jail."),
              p("Same limits", "h2"),
              p("Every harness runs with its own shipped limits under the same wall cap per task, with two "
                "exceptions. Overseer v5 ships with a 100-step and a $5 budget; omp, pi and dsh have no such caps "
                "and Hermes allows about 500 turns. Five tasks allow around 400 steps, so v5 could have been "
                "stopped at step 100 while the others carried on. We lifted both (--max-steps 100000, "
                "--max-cost 1000), so the wall clock is the only limit for everyone. Approvals are off for every "
                "arm."),
              p("Same moment", "h2"),
              p("All five arms of a task start at the same instant, in a launch order shuffled per task, at the "
                "same process priority. The next task starts only when all five are done. They share the same "
                "provider load, the same machine load and the same hour."),
              p("What still differs, on purpose", "h2"),
              *bullets([
                  "Tools: Overseer v5 offers 10, pi 4, omp 11, Hermes 19, dsh 25.",
                  "Side calls: omp makes a short title call, dsh a small extra call, Hermes probes the endpoint for "
                  "its context size (that probe isn't a model call and isn't counted).",
                  "Recovery: each harness handles errors its own way. Hermes, for example, waits ten minutes after a "
                  "rate limit.",
                  "Temperature, prompts, memory and everything else that makes a harness what it is.",
              ]),
              p("Two honest caveats", "h2"),
              *bullets([
                  "We wrote both this benchmark and Overseer. The rule that nobody building Overseer may see the "
                  "tasks guards against tuning to the test; it can't rule out a task set that leans our way without "
                  "anyone meaning it to.",
                  "One seed is noisy. A single unlucky cell moves a score by up to 3.7 points.",
              ]),
              PageBreak()]

    # ---- 4. grading + wiring checks
    story += [p("4 · Prove the grading works", "h1"),
              p("Before any harness runs, two free checks prove the graders themselves."),
              table([["Check", "What it does", "Result"],
                     ["oracle-check", "applies each task's reference solution and grades it", "27 of 27 score 100"],
                     ["null-check", "does nothing at all and grades the empty result", "27 of 27 score 0"]],
                    [28 * mm, W_TEXT - 68 * mm, 40 * mm]),
              p("A task whose reference fix scored below 100, or whose empty result scored above 0, would be "
                "broken; we'd fix the task before spending anything."),
              Spacer(1, 6),
              p("5 · Prove the wiring", "h1"),
              p("Next, every harness runs the simplest task against a fake provider on this machine, with a dummy "
                "key. Nothing is billed. A harness that tried to bypass its gateway would meet a dead end, and the "
                "check would fail."),
              table([["Harness", "Routed", "Calls", "What left the gateway"],
                     ["Overseer v5", "yes", "1", "deepseek-v4.1-flash, stream, thinking on, effort max, 384,000, 10 tools"],
                     ["omp", "yes", "2", "same settings; one title call with 0 tools, then the task with 11"],
                     ["dsh", "yes", "2", "same settings; 25 tools, then a 0-tool call"],
                     ["pi", "yes", "1", "same settings; 4 tools"],
                     ["Hermes", "yes", "2", "same settings; one non-streamed call, then 19 tools (plus a context probe)"]],
                    [24 * mm, 14 * mm, 12 * mm, W_TEXT - 50 * mm]),
              p("Every request also carried a per-conversation session id, which the provider uses to route cache "
                "hits. All arms get the same cache treatment.", "small"),
              p("The watcher was tested the same way: a full one-task run on all five arms through the fake "
                "provider. Its token counts matched each harness's own for every arm. The test found two bugs "
                "(cells finishing between two checks went unseen; Hermes's context probe was counted as a model "
                "answer), both fixed before the paid run."),
              PageBreak()]

    # ---- 6. watcher
    story += [p("6 · Set up the watcher", "h1"),
              p("A paid run is watched from start to finish. The watcher reads each cell's gateway log every 30 "
                "seconds and writes log sheets for review later. It never reads grades: scores stay sealed until "
                "the final report."),
              table([["File", "What it holds"],
                     ["live.md", "every cell climbing now (calls, errors, input, cache rate, output, peak context, "
                      "cost, seconds since its last model call), plus totals per harness"],
                     ["arm-<harness>.md", "one sheet per harness: every task so far, in order"],
                     ["events.log", "what deserves a look: starts and finishes, failed cells, real 429s, upstream "
                      "errors, three failed answers in a row, ten minutes without model traffic, every $1 of spend, "
                      "every request the gateway had to change"],
                     ["progress.csv", "one row per cell per tick: the time series (1,807 rows)"],
                     ["calls.csv", "one row per model call: status, tokens, time to first byte, duration (3,020 rows)"],
                     ["cells.csv", "one row per finished cell (135 rows)"]],
                    [30 * mm, W_TEXT - 30 * mm]),
              Spacer(1, 6),
              p("On top of the sheets", "h2"),
              *bullets([
                  "An alert stream reads events.log and raises anything that needs action: failures, real 429s, "
                  "upstream errors and stalls. It re-arms every 30 minutes.",
                  "A stall alert is checked against the process list. If that harness's process is still alive, "
                  "the stall is real and gets looked at by hand: its open connections, its last gateway events, its "
                  "child processes. We look; we don't intervene, because the wall cap is the same for everyone.",
                  "Each cell keeps its full gateway log in its results folder, so the record outlives the run.",
                  "The Mac is kept awake for the run, and the harnesses run a little below the owner's own apps.",
              ]),
              p("A lesson from this run", "h2"),
              p("The runner reports a task's five results in launch order once the whole task is done, so a fast "
                "arm can sit finished for minutes while its line waits behind a slower one. The first version of "
                "the watcher took that silence for a stall: 17 stall alerts fired, and 16 were arms that had "
                "already finished. We switched the alert stream to check the process list during the run, and "
                "the watcher now marks a cell as ended as soon as its private folder is removed."),
              PageBreak()]

    # ---- 7. running + oversight
    story += [p("7 · Run it", "h1"),
              p("The run started at 04:01 UTC, one minute after Go's early double-price window closed, and finished "
                "at 07:30 UTC. Tasks ran one after another; inside each task, the five harnesses ran side by side."),
              fig("lockstep", caption="Each block is one harness on one task. A task ends when its slowest harness "
                  f"finishes, so the gaps on the faster rows are waiting time. Overseer v5 was the slowest arm on "
                  f"{N['slowest_count']['overseer']} of 27 tasks."),
              p("Settings for this run", "h2"),
              table([["Setting", "Value"],
                     ["command", "obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 1 --run-set ob1-pilot-20261105"],
                     ["mode", "lockstep: the five arms of a task start together; tasks run in order"],
                     ["provider", "OpenCode Go, deepseek-v4.1-flash, through one metered gateway per cell"],
                     ["limits", "each task's wall cap (5 to 90 minutes); no step or cost caps"],
                     ["spend stop", "none (owner's call for the pilot); the watcher reports every $1"]],
                    [26 * mm, W_TEXT - 26 * mm]),
              Spacer(1, 6),
              p("8 · Oversee it", "h1"),
              p("What came up during the run, and what we did about it."),
              table([["Time (UTC)", "What happened", "What we did"],
                     ["04:01", "run started; first cells calling within 30 seconds", "armed the alert stream"],
                     ["04:23–05:02", "stall alerts for pi, omp, Hermes and dsh", "each arm's process had already "
                      "exited: false alarms; switched to process-checked alerts"],
                     ["04:26", "first spot check: $0.19 spent after 25 minutes, 0 errors", "none needed"],
                     ["05:31", "spend passed $1 after nine tasks", "on track for the estimate"],
                     ["06:45", "real stall: omp silent for 10 minutes with its process alive",
                      "checked its connections and gateway log: it was waiting out the task's own injected "
                      "429 faults and resumed by itself; no action"],
                     ["07:19", "Overseer v5 reached the 15-minute cap on ver-dont-trust-the-fix",
                      "recorded; the cap applies to every arm alike"],
                     ["07:30", "last cell finished; runner exited cleanly", "pulled the blind report"]],
                    [22 * mm, 62 * mm, W_TEXT - 84 * mm]),
              p("Across the whole run: 0 failed cells, 0 infrastructure errors and 0 non-success answers from the "
                "provider. The only 429s were the ones tasks inject on purpose.", "small"),
              PageBreak()]

    # ---- 9. results
    rows = [["Harness", "Approved", "95% interval", "Raw", "Solved", "Gates", "Reliable categories",
             "Spend"]]
    for a in ARMS:
        r = R[a]
        rows.append([NAME[a], f"{r['approved']:.1f}", f"{r['lo']:.1f}–{r['hi']:.1f}", f"{r['raw']:.1f}",
                     f"{r['solved']}/27", str(r["gates"]), f"{r['reliable']}/15", money(P[a]["usd"])])
    story += [p("9 · What it measured", "h1"),
              p("The blind report: suite totals only. Which tasks or checks each harness failed stays sealed."),
              table(rows, [24 * mm, 18 * mm, 24 * mm, 13 * mm, 15 * mm, 13 * mm, 30 * mm, W_TEXT - 137 * mm]),
              Spacer(1, 6),
              fig("scores", caption="Approved is the headline: points count only when none of the 15 judges "
                  "rejects the cell. The ring is the raw score before the panel. The whiskers are wide because "
                  "this is one seed."),
              p("How to read it", "h2"),
              *bullets([
                  "omp leads on approved score (51.6), and all five intervals overlap. One seed can't separate them.",
                  "The gap between raw and approved is the panel at work: Overseer v5 scored 71.6 raw but 29.6 "
                  "approved, so judges rejected many of its otherwise-passing cells. Hermes shows the same pattern "
                  "(85.9 raw, 36.8 approved).",
                  "No harness breached a safety gate, and no cell failed for infrastructure reasons.",
                  "None reached the summit (every category reliable at once); the benchmark needs three seeds "
                  "before it can call any category reliable.",
              ]),
              PageBreak(),
              p("Cost and tokens", "h2"),
              fig("spend", caption="Metered at Go's off-peak price list ($0.15 / $0.003 / $0.60 per million "
                  "uncached in, cached in and out). Part of the run fell in Go's 06:00–10:00 UTC double-rate "
                  "window, so the quota it used is somewhat higher than this."),
              fig("tokens", caption="Most input is served from the provider's cache for every harness (90–95%). "
                  "Overseer v5 read 37.4M input tokens over 1,137 calls, about three times the next harness."),
              fig("cumulative", caption="Spend over the run, per harness."),
              PageBreak(),
              fig("heat-wall", width=W_TEXT * 0.92, caption="Wall time per task. Darker is longer; the scale is "
                  "logarithmic, so a short task and a long one are both readable."),
              PageBreak(),
              fig("heat-tokens", width=W_TEXT * 0.92, caption="Tokens per task as each harness counted them, input "
                  "and output together."),
              PageBreak(),
              fig("ttfb", caption="How long the provider took to start answering. Every harness saw about the same "
                  "service (medians 1.2–1.6 s), which is what lockstep is for."),
              p("Per harness, in numbers", "h2"),
              table([["Harness", "Calls", "Input", "Cached", "Output", "Peak context", "Injected faults met",
                      "Busy time", "Longest task"]] +
                    [[NAME[a], f"{P[a]['calls']:,}", f"{P[a]['prompt'] / 1e6:.1f}M",
                      f"{100 * P[a]['cached'] / P[a]['prompt']:.0f}%", f"{P[a]['out'] / 1e3:,.0f}K",
                      f"{P[a]['peak'] / 1e3:,.0f}K", str(P[a]["faults"]), f"{P[a]['wall_h']:.1f} h",
                      f"{P[a]['longest']} ({P[a]['longest_s'] / 60:.0f} min)"] for a in ARMS],
                    [21 * mm, 12 * mm, 13 * mm, 13 * mm, 14 * mm, 17 * mm, 18 * mm, 15 * mm, W_TEXT - 123 * mm]),
              p("Injected faults are the provider errors that chaos tasks throw on purpose; a harness that makes "
                "more calls during a storm meets more of them.", "small"),
              PageBreak()]

    # ---- 10. limits + next
    story += [p("10 · What this pilot tells us, and what it doesn't", "h1"),
              p("It tells us", "h2"),
              *bullets([
                  "The machinery works end to end: 135 cells, no failures, every call metered, every harness on the "
                  "same model and settings.",
                  f"Real costs: {money(tot_usd)} for one seed of all five harnesses, in 3 h 29 m.",
                  "Where time and tokens go per harness and per task, which the 3-seed run can now be planned on.",
              ]),
              p("It doesn't tell us", "h2"),
              *bullets([
                  "Which harness is best. With one seed every interval overlaps, and the benchmark won't call a "
                  "category reliable on fewer than three.",
                  "Why a harness lost points. That stays sealed by design; the transcripts are kept for upkeep of "
                  "the benchmark only.",
              ]),
              p("Next: the three-seed run", "h2"),
              p(f"At the pilot's rate, three seeds cost about {money(tot_usd * 3)} of metered spend and take about "
                "10 to 11 hours in lockstep. Scheduled outside Go's double-rate windows, that's two sittings: one "
                "from 10:00 UTC, and one overnight from 04:01 UTC. The watcher, the alert stream and this report's "
                "charts all run again unchanged."),
              p("11 · Repeat it yourself", "h1"),
              table([["Step", "Command"],
                     ["list the tasks", "python3 obench.py list"],
                     ["prove the graders", "python3 obench.py oracle-check && python3 obench.py null-check"],
                     ["prove the wiring (free)", "source env-go.sh && python3 obench.py wiring --agents overseer,omp,dsh,pi,hermes"],
                     ["run (paid)", "source env-go.sh --with-key && python3 obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 3"],
                     ["watch", "python3 lib/watch.py --run-set <id> --runner-log <file> --runner-pid <pid> --out <dir>"],
                     ["report (blind)", "python3 obench.py report --run-set <id> [--by-category]"],
                     ["this document", "uv run --no-project --with matplotlib python -I charts.py, then "
                      "uv run --no-project --with reportlab python -I build.py"]],
                    [34 * mm, W_TEXT - 34 * mm]),
              Spacer(1, 6),
              p("Everything from this run lives in results/watch/ob1-pilot-20261105 (the log sheets) and "
                "results/runs/ob1-pilot-20261105 (each cell's transcripts, outputs, metrics and gateway log).",
                "small")]

    doc = SimpleDocTemplate(str(HERE / "obench1-pilot-2026-11-05.pdf"), pagesize=A4, leftMargin=20 * mm,
                            rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                            title="OBench1 field run: five-harness pilot", author="Overseer")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


if __name__ == "__main__":
    build()
