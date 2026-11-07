# OBENCH1-CANARY-4f1c9d2a77
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import Grader, WS, load_private, read_bytes, tree_digest

g = Grader()
want = gen.render(gen.commits())
raw = read_bytes(WS / "RELEASE_NOTES.md")
got = raw.decode("utf-8", "replace") if raw is not None else ""
H = {i: gen._hash(i)[:7] for i in range(300)}


def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur and line.startswith("- "):
            out[cur].append(line)
    return out


W, G = sections(want), sections(got)
lines = got.splitlines()
entries = [l for l in lines if l.startswith("- ")]
real = raw is not None and len(entries) >= 50  # nothing below earns credit for an empty file


def line_for(i):
    return next((l for l in want.splitlines() if H[i] in l), None)


def has(i):
    return any(H[i] in l for l in lines)


g.check("RELEASE_NOTES.md matches the reference byte for byte", got == want, 5,
        f"{len(got)} vs {len(want)} chars")
heads = [l for l in lines if l.startswith("#")]
g.check("title and section headings, in order", real and heads == [l for l in want.splitlines() if l.startswith("#")],
        1, heads[:8])
for sec, w in (("Breaking changes", 1.5), ("Features", 1.5), ("Fixes", 1.5)):
    a, b = set(W.get(sec, [])), set(G.get(sec, []))
    g.check(f"{sec}: exactly the right entries", real and a == b, w,
            f"missing {len(a - b)}, extra {len(b - a)}: {sorted(b - a)[:2]}")
g.check("entry order within every section", real and all(G.get(s) == W[s] for s in W), 1, "")
gone = [200, 201, 202, 212, 213, 214, 215]
g.check("reverted commits and the reverts themselves are left out", real and not any(has(i) for i in gone), 1,
        [i for i in gone if has(i)])
g.check("internal scope: non-breaking left out, breaking kept",
        real and not has(90) and not has(91) and line_for(41) in G.get("Breaking changes", []), 0.5, "")
g.check("non-conventional headers and squash bodies are not entries",
        real and not any(has(i) for i in (220, 221, 222, 223)) and "ulk export" not in got, 0.5, "")
g.check("a BREAKING CHANGE footer alone doesn't make a breaking change",
        real and line_for(71) in G.get("Features", []), 0.5, "")
g.check("issue references come only from exact `Fixes #n` lines, only on fixes",
        real and all(line_for(i) in lines for i in (17, 120, 130)), 1, [line_for(i) for i in (17, 120)])
g.check("identical summaries merged (hashes, refs, newest first)",
        real and all(line_for(i) in lines for i in (110, 140)), 1, [line_for(i) for i in (110, 140)])
g.check("long entries shortened with … to exactly the limit, no line over 100 characters",
        real and all(line_for(i) in lines for i in (160, 170)) and max(map(len, lines)) <= 100, 1, "")
order = [l for l in lines if H[205] in l or H[206] in l]
g.check("ordering compares instants, not local timestamp strings",
        real and len(order) == 2 and H[206] in order[0], 0.5, order)
wc = want[want.index("## Contributors"):]
gc = got[got.index("## Contributors"):] if "## Contributors" in got else ""
g.check("Contributors: mailmap, co-authors, no bots, authors only, counts and order", real and gc == wc, 1.5,
        gc.splitlines()[2:5])
g.check("amendments: no Performance section, [perf] in Features, deps written dependencies",
        real and "## Performance" not in got and "**deps:**" not in got
        and line_for(175) in G.get("Features", []) and line_for(53) in G.get("Breaking changes", []), 1, "")
g.check("no trailing whitespace, exactly one final newline",
        real and got.endswith("\n") and not got.endswith("\n\n") and all(l == l.rstrip() for l in lines), 0.5, "")
before = load_private("digest.json", {})
now = tree_digest(WS)
now.pop("RELEASE_NOTES.md", None)
changed = sorted(k for k in set(before) | set(now) if before.get(k) != now.get(k))
g.check("no other file created or changed", real and not changed, 1, changed[:5])
g.done()
