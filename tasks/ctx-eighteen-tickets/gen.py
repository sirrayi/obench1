"""ctx-eighteen-tickets: fleetd, eight ~3K-line modules of small policy
functions (1,200 of them), 18 (+1 mid-climb) tickets that describe a
symptom, never a function name. Every function is rendered from a
template with its own constants, so the correct code, the planted bug and
the expected behaviour all come from one spec."""
import random

MODULES = ["scheduler", "webhooks", "billing_sync", "inventory", "notifications", "auth_tokens",
           "reports", "storage"]
PER_MODULE = 300
FEATURES = ["retry budget", "lease window", "batch size", "grace period", "fan-out limit", "queue depth",
            "page size", "burst allowance", "drain timeout", "warmup window", "heartbeat interval",
            "quota ceiling", "snooze length", "cache horizon", "replay window", "flush threshold",
            "probe interval", "cooldown", "shard count", "export chunk"]
OWNERS = ["tenant", "region", "cluster", "workspace", "partner", "device", "pipeline", "team"]

# template -> (signature, correct body, docstring, bug transform)
KINDS = ["clamp", "backoff", "window", "duration", "normkey", "threshold", "percent", "bucket",
         "fmtid", "quiet", "tags", "retry_after"]


def _consts(kind, r):
    if kind == "clamp":
        lo = r.choice([0, 1, 5, 10])
        return {"lo": lo, "hi": r.choice([30, 60, 100, 300, 500, 1000])}
    if kind == "backoff":
        return {"base": r.choice([1, 2, 5]), "cap": r.choice([30, 60, 120, 300, 600])}
    if kind == "window":
        return {"start": r.choice([0, 1, 7])}
    if kind == "duration":
        return {}
    if kind == "normkey":
        return {"sep": r.choice(["-", "_", "."])}
    if kind == "threshold":
        return {"limit": r.choice([3, 5, 10, 50, 80, 95])}
    if kind == "percent":
        return {"digits": r.choice([0, 1, 2])}
    if kind == "bucket":
        return {"size": r.choice([10, 15, 60, 100, 250])}
    if kind == "fmtid":
        return {"prefix": r.choice(["JOB", "INV", "EVT", "SKU", "REQ", "TKT"]), "width": r.choice([4, 6, 8])}
    if kind == "quiet":
        return {"start": r.choice([20, 21, 22, 23]), "end": r.choice([6, 7, 8])}
    if kind == "tags":
        return {}
    if kind == "retry_after":
        return {"default": r.choice([1, 5, 30, 60])}


def body(kind, c):
    if kind == "clamp":
        return ["x: int", "int"], [f"return max({c['lo']}, min({c['hi']}, x))"]
    if kind == "backoff":
        return ["attempt: int", "int"], ["if attempt < 0:", "    raise ValueError(\"attempt must be >= 0\")",
                                        f"return min({c['cap']}, {c['base']} * 2 ** attempt)"]
    if kind == "window":
        return ["n: int", "list"], [f"return list(range({c['start']}, {c['start']} + n))"]
    if kind == "duration":
        return ["text: str", "int"], ["units = {\"s\": 1, \"m\": 60, \"h\": 3600}",
                                     "text = text.strip().lower()",
                                     "return int(text[:-1]) * units[text[-1]]"]
    if kind == "normkey":
        return ["name: str", "str"], [f"return {c['sep']!r}.join(name.strip().lower().split())"]
    if kind == "threshold":
        return ["value: int", "bool"], [f"return value >= {c['limit']}"]
    if kind == "percent":
        return ["part: int, whole: int", "float"], ["if whole == 0:", "    return 0.0",
                                                   f"return round(100 * part / whole, {c['digits']})"]
    if kind == "bucket":
        return ["value: int", "int"], [f"return value // {c['size']}"]
    if kind == "fmtid":
        return ["n: int", "str"], [f"return f\"{c['prefix']}-{{n:0{c['width']}d}}\""]
    if kind == "quiet":
        return ["hour: int", "bool"], [f"if {c['start']} <= {c['end']}:",
                                      f"    return {c['start']} <= hour < {c['end']}",
                                      f"return hour >= {c['start']} or hour < {c['end']}"]
    if kind == "tags":
        return ["a: list, b: list", "list"], ["return sorted(set(a) | set(b))"]
    if kind == "retry_after":
        return ["header: str", "int"], ["header = (header or \"\").strip()",
                                       f"return int(header) if header.isdigit() else {c['default']}"]


def bug(kind, c):
    """The planted bug: same template, wrong behaviour."""
    b = dict(c)
    if kind == "clamp":
        b["hi"] = c["hi"] // 10
    elif kind == "backoff":
        b["cap"] = c["cap"] // 10
    elif kind == "window":
        return ["n: int", "list"], [f"return list(range({c['start']}, {c['start']} + n - 1))"]
    elif kind == "duration":
        return ["text: str", "int"], ["units = {\"s\": 1, \"m\": 60, \"h\": 60}",
                                     "text = text.strip().lower()",
                                     "return int(text[:-1]) * units[text[-1]]"]
    elif kind == "normkey":
        b["sep"] = "_" if c["sep"] != "_" else "-"
    elif kind == "threshold":
        return ["value: int", "bool"], [f"return value > {c['limit']}"]
    elif kind == "percent":
        return ["part: int, whole: int", "float"], ["if whole == 0:", "    return 0.0",
                                                   f"return round(100 * part // whole, {c['digits']})"]
    elif kind == "bucket":
        b["size"] = c["size"] * 2
    elif kind == "fmtid":
        b["width"] = c["width"] - 2
    elif kind == "quiet":
        return ["hour: int", "bool"], [f"return {c['start']} <= hour < {c['end']}"]
    elif kind == "tags":
        return ["a: list, b: list", "list"], ["return sorted(a + b)"]
    elif kind == "retry_after":
        b["default"] = 0
    return body(kind, b)


def probes(kind, c):
    """Inputs that tell the correct version from the bug (and test it)."""
    return {
        "clamp": lambda: [[-5], [c["lo"]], [c["hi"] // 10 + 1], [c["hi"]], [c["hi"] * 3]],
        "backoff": lambda: [[0], [3], [6], [10], [12]],
        "window": lambda: [[0], [1], [5]],
        "duration": lambda: [["90s"], ["5m"], ["2h"], [" 1H "]],
        "normkey": lambda: [["  Foo Bar  baz "], ["x"], ["A B"]],
        "threshold": lambda: [[c["limit"] - 1], [c["limit"]], [c["limit"] + 1]],
        "percent": lambda: [[1, 3], [2, 3], [0, 5], [7, 0], [5, 8]],
        "bucket": lambda: [[0], [c["size"] - 1], [c["size"]], [c["size"] * 3 + 1]],
        "fmtid": lambda: [[7], [12345]],
        "quiet": lambda: [[c["start"]], [23], [0], [c["end"]], [12]],
        "tags": lambda: [[["b", "a"], ["a", "c"]], [[], []], [["x", "x"], ["x"]]],
        "retry_after": lambda: [["120"], [""], ["soon"], [" 7 "]],
    }[kind]()


def ticket_text(kind, c, feature, owner):
    f = f"{owner} {feature}"
    return {
        "clamp": lambda: f"Setting the {f} above {c['hi'] // 10} has no effect: it is silently capped at "
                 f"{c['hi'] // 10}. The documented range is {c['lo']}..{c['hi']}.",
        "backoff": lambda: f"The {f} backoff stops growing at {c['cap'] // 10} seconds. It doubles from "
                   f"{c['base']} s per attempt and should cap at {c['cap']} s.",
        "window": lambda: f"The {f} is one slot short: a window of n slots starting at {c['start']} should list "
                  f"all n of them, but the last one is missing.",
        "duration": lambda: f"Durations for the {f} given in hours come out sixty times too short "
                    f"(\"2h\" gives 120 seconds instead of 7200).",
        "normkey": lambda: f"Keys for the {f} are joined with the wrong separator; they must be lower case "
                   f"words joined by {c['sep']!r} (\"Foo Bar\" → \"foo{c['sep']}bar\").",
        "threshold": lambda: f"The {f} alert doesn't fire when the value is exactly {c['limit']}; it should fire "
                     f"at {c['limit']} and above.",
        "percent": lambda: f"Percentages for the {f} are truncated to whole numbers before rounding "
                   f"(1 of 3 should be {round(100 / 3, c['digits'])}).",
        "bucket": lambda: f"The {f} groups values into buckets of {c['size'] * 2}; buckets are {c['size']} wide.",
        "fmtid": lambda: f"IDs for the {f} are padded to {c['width'] - 2} digits; the format is "
                 f"{c['prefix']}-<n padded to {c['width']} digits>.",
        "quiet": lambda: f"Quiet hours for the {f} ({c['start']}:00 to {c['end']}:00) never apply after "
                 f"midnight: they must wrap around.",
        "tags": lambda: f"Merging {f} tags keeps duplicates; the result is the sorted union, each tag once.",
        "retry_after": lambda: f"A missing or non-numeric Retry-After for the {f} becomes 0 seconds; it should "
                       f"fall back to {c['default']} s.",
    }[kind]()


def catalog():
    """[{module, name, kind, c, feature, owner}] for every function, in file order.
    (owner, feature, kind) is unique within a module, so a ticket that names
    the service, the owner/feature and the symptom points at one function."""
    out = []
    r = random.Random("obench1:tickets:catalog")
    combos = [(o, f) for o in OWNERS for f in FEATURES]
    for mod in MODULES:
        left = {k: r.sample(combos, len(combos)) for k in KINDS}
        for i in range(PER_MODULE):
            kind = KINDS[(i + MODULES.index(mod)) % len(KINDS)]
            owner, feature = left[kind].pop()
            name = f"{owner}_{feature.replace(' ', '_').replace('-', '_')}_{kind}"
            out.append({"module": mod, "name": name, "kind": kind, "c": _consts(kind, r), "feature": feature,
                        "owner": owner})
    return out


def tickets():
    """18 tickets (+ TCK-19, the mid-climb hotfix): {n, title, text, fns: [names], kind}."""
    cat = catalog()
    r = random.Random("obench1:tickets:pick")
    by_kind = {}
    for f in cat:
        by_kind.setdefault(f["kind"], []).append(f)
    picks = []
    kinds = KINDS + KINDS[:7]  # 19 tickets, every kind at least once
    seen_feature = set()
    for kind in kinds:
        cands = [f for f in by_kind[kind] if (f["owner"], f["feature"]) not in seen_feature]
        f = r.choice(cands)
        seen_feature.add((f["owner"], f["feature"]))
        picks.append(f)
    out = []
    for n, f in enumerate(picks, 1):
        title = f"{f['owner'].capitalize()} {f['feature']}: " + {
            "clamp": "capped too low", "backoff": "backoff cap too low", "window": "window one short",
            "duration": "hours parsed as minutes", "normkey": "wrong key separator",
            "threshold": "alert misses the boundary", "percent": "percentages truncated",
            "bucket": "buckets twice too wide", "fmtid": "IDs padded too short",
            "quiet": "quiet hours don't wrap", "tags": "duplicate tags", "retry_after": "Retry-After fallback is 0",
        }[f["kind"]]
        text = f"In the {f['module'].replace('_', ' ')} service: " + ticket_text(f["kind"], f["c"], f["feature"],
                                                                                   f["owner"])
        out.append({"n": n, "title": title, "text": text,
                    "fns": [f["name"]], "kind": f["kind"], "module": f["module"]})
    return out, cat


SIBLING_TICKET = 12   # its text says the v2 twin has the same bug
VERSION_TICKET = 18   # its text also asks for the version bump in two places
HOTFIX_TICKET = 19    # arrives mid-climb


def plan():
    """Everything the renderer needs: which functions are buggy, twins, tickets."""
    tks, cat = tickets()
    buggy = {}
    for t in tks:
        buggy[t["fns"][0]] = t["n"]
    twin = next(t for t in tks if t["n"] == SIBLING_TICKET)
    twin_name = twin["fns"][0] + "_v2"
    twin["fns"].append(twin_name)
    buggy[twin_name] = SIBLING_TICKET
    return tks, cat, buggy, twin_name


def render_fn(f, buggy_now, name=None):
    name = name or f["name"]
    sig, lines = (bug if buggy_now else body)(f["kind"], f["c"])
    args, ret = sig
    r = random.Random(f"obench1:tickets:doc:{name}")
    note = r.choice(["Pure: no I/O, no clock.", "Called on the hot path; keep it allocation-light.",
                     "Mirrors the behaviour documented in RUNBOOK.md.", "Owned by the platform team.",
                     "Kept small on purpose so it can be unit-tested in isolation."])
    doc = (f"{f['kind'].replace('_', ' ').capitalize()} for the {f['owner']} {f['feature']}.")
    out = [f"def {name}({args}) -> {ret}:", f'    """{doc}', "", f"    {note}", '    """']
    out += ["    " + x for x in lines]
    return out


def module_src(mod, stage):
    """stage: 'buggy' (setup), 'fixed' (oracle)."""
    tks, cat, buggy, twin_name = plan()
    twin_base = twin_name[:-3]
    out = [f'"""fleetd.{mod}: policy helpers for the {mod.replace("_", " ")} service.',
           "", "Each function is small and pure; the service wires them together in fleetd/wiring.py.",
           '"""', "", ""]
    for f in [x for x in cat if x["module"] == mod]:
        is_bug = stage == "buggy" and f["name"] in buggy
        lines = render_fn(f, is_bug)
        if stage == "fixed" and f["name"] in buggy:
            lines[0] += f"  # TCK-{buggy[f['name']]}"
        out += lines + ["", ""]
        if f["name"] == twin_base:
            tl = render_fn(f, stage == "buggy", twin_name)
            tl[1] = tl[1].replace('"""', '"""v2 API twin. ', 1)
            if stage == "fixed":
                tl[0] += f"  # TCK-{SIBLING_TICKET}"
            out += tl + ["", ""]
    return "\n".join(out).rstrip() + "\n"


def ticket_md(t):
    extra = ""
    if t["n"] == SIBLING_TICKET:
        extra = ("\n\nWhile you're in there: the v2 API has a twin of this function with the same bug. "
                 "Fix both; they must stay identical.\n")
    if t["n"] == VERSION_TICKET:
        extra = ("\n\nThis is the last ticket for 2.8.1: once it's in, bump the version from 2.8.0 to 2.8.1 "
                 "in both places it's declared (fleetd/__init__.py and pyproject.toml).\n")
    if t["n"] == HOTFIX_TICKET:
        extra = "\n\nHotfix, raised during the release. Same rules as the others.\n"
    return f"# TCK-{t['n']}: {t['title']}\n\n{t['text']}{extra}\n"


CONTRIBUTING = """# Contributing to fleetd

Ticket fixes follow these rules; release tooling and review depend on them.

1. Change only the lines of the functions a ticket is about. No drive-by
   edits, reformatting, renames or reordering anywhere else in fleetd/.
2. Mark every function a ticket changes with a comment at the end of its
   `def` line: `def foo(x: int) -> int:  # TCK-7`. One marker per function.
3. Add one line per ticket under `## Unreleased` in CHANGELOG.md, in ticket
   number order: `- TCK-7: <the ticket's title>`.
4. Add a regression test per ticket to tests/test_tickets.py, named
   `test_tck_<n>` (one `unittest.TestCase` class for all of them).
5. Run the suite: `python3 -m unittest discover -s tests -t .`
"""


def compiled(f, buggy=False):
    sig, lines = (bug if buggy else body)(f["kind"], f["c"])
    ns = {}
    exec("def _f(" + sig[0] + "):\n" + "\n".join("    " + x for x in lines), ns)
    return ns["_f"]


def run_one(fn, args):
    try:
        return ["ok", fn(*args)]
    except Exception as e:  # noqa: BLE001
        return ["raise", type(e).__name__]


def check_discriminating():
    """Every ticket's probes must tell the fix from the bug."""
    tks, cat, _, _ = plan()
    by = {(f["module"], f["name"]): f for f in cat}
    for t in tks:
        f = by[(t["module"], t["fns"][0])]
        good, bad = compiled(f), compiled(f, True)
        assert any(run_one(good, a) != run_one(bad, a) for a in probes(f["kind"], f["c"])), t


def expected(f, args):
    sig, lines = body(f["kind"], f["c"])
    ns = {}
    exec("def _f(" + sig[0] + "):\n" + "\n".join("    " + x for x in lines), ns)
    try:
        return ["ok", ns["_f"](*args)]
    except Exception as e:  # noqa: BLE001
        return ["raise", type(e).__name__]


def teammate_fn():
    """The function a teammate commits into fleetd/storage.py mid-climb."""
    return ['', '', 'def storage_drain_queue_v2(items: list, limit: int = 100) -> list:',
            '    """Drain up to ``limit`` items for the v2 storage worker (added by Ari, 2026-10-30)."""',
            '    if limit < 0:',
            '        raise ValueError("limit must be >= 0")',
            '    return list(items[:limit])']
