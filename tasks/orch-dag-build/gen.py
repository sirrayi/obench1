"""orch-dag-build: eight record normalizers, one per service, each written
from its own spec of ~20-30 ordered rules; five services depend on another's
normalizer (a DAG three deep). Big, parallel, mechanical work: fan it out or
build an engine, but be quick (wall-time check) and keep up with an
amendment that lands mid-run."""
import datetime
import json
import random
from decimal import ROUND_HALF_UP, Decimal

SVCS = ["accounts", "billing", "shipments", "customers", "contacts", "invoices", "payments", "returns"]
DEPS = {"customers": "accounts", "contacts": "customers", "invoices": "billing", "payments": "invoices", "returns": "shipments"}
WORDS = ["name", "email", "city", "country", "tier", "note", "code", "owner", "region", "label", "ref", "status",
         "tags", "since", "amount", "fee", "active", "vip", "due"]
KIND = {"amount": "money", "fee": "money", "active": "flag", "vip": "flag", "since": "date", "due": "date", "tags": "list"}
DEFAULTS = {"text": "unknown", "money": "0.00", "flag": "no", "date": "01/01/2000", "list": ""}
AMENDED = "invoices"
TASK = ("Write the eight record normalizers described in specs/: `clients/<service>.py` exposing "
        "`normalize(record: dict) -> dict`, one per spec, following specs/RULES.md. examples/ has a few worked "
        "examples per service. Specs can change while you work; the current spec is what counts. Be quick about it.")
RULES_MD = """# Rule meanings

Rules apply in order to a copy of the record. A rule on a field that isn't there does nothing, except `require` and `default`.

- require `f`: raise ValueError if `f` is missing.
- default `f` = "v": if `f` is missing, set it to the string v.
- strip `f` / lower `f` / upper `f`: the string method of that name.
- rename `a` -> `b`: move the value of `a` to `b`.
- drop `f`: remove `f`.
- cents `f`: the value (a number or a numeric string, maybe with spaces) as integer cents, rounded half up.
- bool `f`: yes/true/1 -> true, no/false/0 -> false, case-insensitive, spaces ignored; anything else raises ValueError.
- iso-date `f`: `DD/MM/YYYY` (spaces ignored) -> `YYYY-MM-DD`; an invalid date raises ValueError.
- split `f` on "s": split on s, strip each piece, drop empty pieces; the result is a list.

"Depends on X" means: apply X's normalize to the record first, then this spec's rules.
An amendment that "supersedes rule N" replaces rule N.
"""


def rules(svc):
    r = random.Random("obench1:dag:" + svc)
    per = []
    for w in r.sample(WORDS, 9):
        name, kind = f"{svc[:3]}_{w}", KIND.get(w, "text")
        ops = []
        x = r.random()
        if x < 0.3:
            ops.append(("require", name))
        elif x < 0.6:
            ops.append(("default", name, DEFAULTS[kind]))
        if kind == "text":
            ops += [(op, name) for op in r.sample(["strip", "lower", "upper"], r.randint(1, 3))]
        elif kind == "money":
            ops.append(("cents", name))
        elif kind == "flag":
            ops.append(("bool", name))
        elif kind == "date":
            ops.append(("iso-date", name))
        else:
            ops.append(("split", name, r.choice([",", ";", "|"])))
        y = r.random()
        if y < 0.35:
            new = f"{svc}_{w}"
            at = r.randint(len(ops) - 1 if ops[0][0] in ("require", "default") else 0, len(ops))
            at = max(at, 1 if ops[0][0] in ("require", "default") else 0)
            ops = ops[:at] + [("rename", name, new)] + [(o[0], new, *o[2:]) for o in ops[at:]]
        elif y < 0.45:
            ops.append(("drop", ops[-1][1]))
        per.append(ops)
    out = []
    while any(per):
        i = r.choice([k for k, o in enumerate(per) if o])
        out.append(per[i].pop(0))
    return out


def amendment():
    """(rule number, new rule): the first case rule whose flip changes results."""
    rs = rules(AMENDED)
    sample = records(AMENDED, 80, "amend")
    for n, o in enumerate(rs):
        if o[0] not in ("lower", "upper"):
            continue
        flip = ("upper" if o[0] == "lower" else "lower", o[1])
        new = rs[:n] + [flip] + rs[n + 1:]
        if any(outcome(lambda x: apply(new, normalize(DEPS[AMENDED], x)), r) != outcome(lambda x: normalize(AMENDED, x, False), r)
               for r in sample):
            return n + 1, flip
    raise AssertionError("no amendment changes anything")


def current(svc, amended=True):
    rs = rules(svc)
    if amended and svc == AMENDED:
        n, op = amendment()
        rs[n - 1] = op
    return rs


def render(op):
    k, f = op[0], op[1]
    if k == "default":
        return f'default `{f}` = "{op[2]}"'
    if k == "rename":
        return f"rename `{f}` -> `{op[2]}`"
    if k == "split":
        return f'split `{f}` on "{op[2]}"'
    return f"{k} `{f}`"


def spec(svc):
    dep = f"Depends on {DEPS[svc]}: apply `clients/{DEPS[svc]}.py`'s normalize first." if svc in DEPS else "Depends on nothing."
    body = "\n".join(f"{i}. {render(op)}" for i, op in enumerate(rules(svc), 1))
    return f"# {svc}\n\nNormalize one raw {svc} record. {dep}\n\n{body}\n"


def amendment_text():
    n, op = amendment()
    return f"\n## Amendment 1 (from the service owner; supersedes rule {n})\n\n{n}. {render(op)}\n"


def apply(rs, rec):
    rec = dict(rec)
    for op in rs:
        k, f = op[0], op[1]
        if k == "require":
            if f not in rec:
                raise ValueError(f"missing {f}")
            continue
        if k == "default":
            rec.setdefault(f, op[2])
            continue
        if f not in rec:
            continue
        v = rec[f]
        if k in ("strip", "lower", "upper"):
            rec[f] = getattr(v, k)()
        elif k == "rename":
            rec[op[2]] = rec.pop(f)
        elif k == "drop":
            del rec[f]
        elif k == "cents":
            rec[f] = int(Decimal(str(v).strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
        elif k == "bool":
            s = str(v).strip().lower()
            if s not in ("yes", "true", "1", "no", "false", "0"):
                raise ValueError(f"bad flag {v!r}")
            rec[f] = s in ("yes", "true", "1")
        elif k == "iso-date":
            rec[f] = datetime.datetime.strptime(v.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
        elif k == "split":
            rec[f] = [p.strip() for p in v.split(op[2]) if p.strip()]
    return rec


def normalize(svc, rec, amended=True):
    if svc in DEPS:
        rec = normalize(DEPS[svc], rec, amended)
    return apply(current(svc, amended), rec)


def raw_fields(svc):
    out = {}
    while True:
        for op in rules(svc):
            if op[1].startswith(svc[:3] + "_"):
                out[op[1]] = KIND.get(op[1].split("_", 1)[1], "text")
        if svc not in DEPS:
            return out
        svc = DEPS[svc]


def value(kind, r):
    if kind == "text":
        word = r.choice(["Alpha", "beta GROUP", "Delta-9", "ünïcode Café", "x", "Mixed Case"])
        return r.choice(["", " ", "  "]) + word + r.choice(["", " ", "\t"])
    if kind == "money":
        return r.choice([str(round(r.uniform(0, 500), 3)), f" {r.randint(0, 99)}.{r.randint(0, 999):03d} ",
                         round(r.uniform(0, 500), 2), r.randint(0, 900), "2.675", "0.005"])
    if kind == "flag":
        return r.choice(["Yes", "no", " TRUE ", "false", "1", "0", "yes ", "maybe" if r.random() < 0.15 else "No"])
    if kind == "date":
        if r.random() < 0.08:
            return "31/02/2026"
        d = datetime.date(2020, 1, 1) + datetime.timedelta(days=r.randint(0, 2500))
        return r.choice(["", " "]) + d.strftime("%d/%m/%Y")
    return r.choice([",", ";", "|"]).join(r.choice(["a", " b", "c ", "", "dd", " e e "]) for _ in range(r.randint(0, 5)))


def records(svc, n, salt):
    r = random.Random(f"obench1:dag:rec:{svc}:{salt}")
    fields = raw_fields(svc)
    out = []
    for _ in range(n):
        rec = {}
        for f, kind in fields.items():
            if r.random() > 0.12:
                rec[f] = value(kind, r)
        out.append(rec)
    return out


def outcome(fn, rec):
    try:
        return {"ok": fn(rec)}
    except ValueError:
        return {"err": "ValueError"}
