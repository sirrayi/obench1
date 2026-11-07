"""lh-money-migration: a 40-module float-money codebase (setup), the same
codebase on Money (oracle), and the hidden cases (grader). Both renderings
come from one spec, so names and parameter lists match by construction,
and `expect` mirrors the Money rendering's arithmetic in plain Decimal."""
import datetime
import json
import random
import re
from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

PACKAGES = [
    ("invoices", "ROUND_HALF_UP", ["lines", "discounts", "subtotals", "credits", "deposits"]),
    ("billing", "ROUND_HALF_UP", ["plans", "proration", "usage", "overage", "coupons"]),
    ("tax", "ROUND_HALF_UP", ["vat", "sales_tax", "withholding", "exemptions", "reverse_charge"]),
    ("fx", "ROUND_HALF_EVEN", ["convert", "quotes", "revaluation", "cross_rates", "spreads"]),
    ("interest", "ROUND_HALF_EVEN", ["accrual", "late_fees", "savings", "loans", "penalties"]),
    ("refunds", "ROUND_DOWN", ["partial", "chargebacks", "returns", "goodwill", "cancellations"]),
    ("payouts", "ROUND_HALF_UP", ["splits", "commissions", "holdbacks", "transfers", "fees"]),
    ("reports", "ROUND_HALF_UP", ["summaries", "aging", "statements"]),
    ("export", "ROUND_HALF_UP", ["json_export", "csv_export"]),
]
NOUN = {
    "lines": "line", "discounts": "discount", "subtotals": "subtotal", "credits": "credit",
    "deposits": "deposit", "plans": "plan", "proration": "prorated", "usage": "usage",
    "overage": "overage", "coupons": "coupon", "vat": "vat", "sales_tax": "sales_tax",
    "withholding": "withholding", "exemptions": "exemption", "reverse_charge": "reverse_charge",
    "convert": "conversion", "quotes": "quote", "revaluation": "revaluation", "cross_rates": "cross",
    "spreads": "spread", "accrual": "accrual", "late_fees": "late_fee", "savings": "savings",
    "loans": "loan", "penalties": "penalty", "partial": "partial_refund", "chargebacks": "chargeback",
    "returns": "return", "goodwill": "goodwill", "cancellations": "cancellation", "splits": "split",
    "commissions": "commission", "holdbacks": "holdback", "transfers": "transfer", "fees": "fee",
    "summaries": "summary", "aging": "aging", "statements": "statement",
    "json_export": "json", "csv_export": "csv", "instant": "instant_payout",
}
MODES = {"ROUND_HALF_UP": ROUND_HALF_UP, "ROUND_HALF_EVEN": ROUND_HALF_EVEN, "ROUND_DOWN": ROUND_DOWN}
MINOR = {"USD": 2, "EUR": 2, "GBP": 2, "CHF": 2, "JPY": 0, "KWD": 3}
BASE = {"USD": "1", "EUR": "0.92130", "GBP": "0.78640", "JPY": "151.420", "KWD": "0.30710", "CHF": "0.88050"}
GENERAL = ["scale", "pct", "total", "net", "cap", "split", "accrue", "settled", "exceeds", "format"]


def rates():
    """(src, dst) -> rate text, 5 significant digits, trailing zeros kept."""
    out = {}
    for a in BASE:
        for b in BASE:
            if a == b:
                continue
            if a == "USD":
                out[(a, b)] = BASE[b]
                continue
            d = Decimal(BASE[b]) / Decimal(BASE[a])
            out[(a, b)] = str(d.quantize(Decimal(1).scaleb(d.adjusted() - 4), ROUND_HALF_EVEN))
    return out


RATES = rates()


def rates_csv():
    return "src,dst,rate\n" + "".join(f"{a},{b},{r}\n" for (a, b), r in RATES.items())


def q(x, cur, mode):
    return x.quantize(Decimal(1).scaleb(-MINOR[cur]), rounding=mode)


AMENDED = {"payouts": "ROUND_HALF_EVEN"}  # AMENDMENTS/001, if it fired
INSTANT = ("payouts", "instant")  # the teammate's module, if it landed


def layout(amended=False, instant=False):
    """[(pkg, mod, R)] for the repo as the grader sees it after the avalanches."""
    out = []
    for pkg, R, mods in PACKAGES:
        R = AMENDED.get(pkg, R) if amended else R
        for mod in mods + (["instant"] if instant and pkg == INSTANT[0] else []):
            out.append((pkg, mod, R))
    return out


def module_kinds(pkg, mod):
    if mod == "instant":
        return ["pct", "split", "format", "exceeds"]
    if pkg == "export":
        return [mod, "format", "total"]
    r = random.Random(f"obench1:money:{pkg}.{mod}")
    picks = r.sample(GENERAL, 5)
    if pkg == "fx":
        picks = ["convert", "quote"] + picks[:3]
    if mod == "convert":
        picks.append("convert_float")
    return picks


def func_spec(kind, n):
    """Name, params [(name, float_ann, dec_ann, default)], return anns, doc,
    validation, float body, Money body (with {R} for the rounding mode)."""
    h = n.replace("_", " ")
    S = {
        "scale": (f"scaled_{n}", [("amount", "MoneyF", "Money", None), ("factor", "Rate", "Decimal", None),
                                   ("currency", "str", "str", None)], ("MoneyF", "Money"),
                  f"The {h} amount multiplied by ``factor``, rounded to the currency's minor unit.",
                  ["if factor < 0:", '    raise ValueError("factor must not be negative")'],
                  ["return round_money(amount * factor, currency)"],
                  ["return (amount * factor).round({R})"]),
        "pct": (f"percent_of_{n}", [("amount", "MoneyF", "Money", None), ("pct", "Rate", "Decimal", None),
                                     ("currency", "str", "str", None)], ("MoneyF", "Money"),
                f"``pct`` percent of the {h} amount, rounded to the currency's minor unit.",
                ["if not 0 <= pct <= 100:", '    raise ValueError("pct must be between 0 and 100")'],
                ["return round_money(amount * pct / 100, currency)"],
                ["return (amount * pct / 100).round({R})"]),
        "total": (f"total_{n}", [("amounts", "list", "list", None), ("currency", "str", "str", None)],
                  ("MoneyF", "Money"),
                  f"The sum of several {h} amounts (zero for none), rounded to the minor unit.",
                  [],
                  ["return round_money(sum(amounts), currency)"],
                  ["return Money.sum(amounts, currency).round({R})"]),
        "net": (f"net_{n}", [("gross", "MoneyF", "Money", None), ("pct", "Rate", "Decimal", None),
                             ("currency", "str", "str", None)], ("MoneyF", "Money"),
                f"The {h} gross amount less ``pct`` percent of it. Only the deduction is rounded.",
                ["if not 0 <= pct <= 100:", '    raise ValueError("pct must be between 0 and 100")'],
                ["return gross - round_money(gross * pct / 100, currency)"],
                ["return gross - (gross * pct / 100).round({R})"]),
        "cap": (f"capped_{n}", [("amount", "MoneyF", "Money", None), ("pct", "Rate", "Decimal", None),
                                ("cap", "MoneyF", "Money", None), ("currency", "str", "str", None)],
                ("MoneyF", "Money"),
                f"``pct`` percent of the {h} amount, rounded, but never more than ``cap``.",
                ["if not 0 <= pct <= 100:", '    raise ValueError("pct must be between 0 and 100")'],
                ["return min(round_money(amount * pct / 100, currency), cap)"],
                ["return min((amount * pct / 100).round({R}), cap)"]),
        "split": (f"split_{n}", [("amount", "MoneyF", "Money", None), ("parts", "int", "int", "2"),
                                 ("currency", "str", "str", '"USD"')], ("list", "list"),
                  f"The {h} amount in ``parts`` equal rounded shares; the last share takes the remainder.",
                  ["if parts <= 0:", '    raise ValueError("parts must be positive")'],
                  ["share = round_money(amount / parts, currency)",
                   "return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]"],
                  ["share = (amount / parts).round({R})",
                   "return [share] * (parts - 1) + [(amount - share * (parts - 1)).round({R})]"]),
        "accrue": (f"accrued_{n}", [("balance", "MoneyF", "Money", None), ("annual_rate", "Rate", "Decimal", None),
                                    ("days", "int", "int", "30"), ("currency", "str", "str", '"USD"')],
                   ("MoneyF", "Money"),
                   f"Simple {h} interest on ``balance`` for ``days`` days at ``annual_rate`` percent "
                   "a year (actual/365), rounded to the minor unit.",
                   ["if days < 0:", '    raise ValueError("days must not be negative")'],
                   ["return round_money(balance * annual_rate / 100 * days / 365, currency)"],
                   ["return (balance * annual_rate / 100 * days / 365).round({R})"]),
        "settled": (f"{n}_settled", [("paid", "MoneyF", "Money", None), ("due", "MoneyF", "Money", None)],
                    ("bool", "bool"),
                    f"Whether the {h} has been paid in full.",
                    [],
                    ["return abs(paid - due) < 0.005"],
                    ["return paid == due"]),
        "exceeds": (f"{n}_exceeds", [("amount", "MoneyF", "Money", None), ("limit", "MoneyF", "Money", None)],
                    ("bool", "bool"),
                    f"Whether the {h} amount is over ``limit``.",
                    [],
                    ["return amount > limit"],
                    ["return amount > limit"]),
        "format": (f"format_{n}", [("amount", "MoneyF", "Money", None), ("currency", "str", "str", None)],
                   ("str", "str"),
                   f"The {h} amount as display text, e.g. ``12.30 USD``.",
                   [],
                   ['return "%.*f %s" % (EXPONENT[currency], amount, currency)'],
                   ['return "%s %s" % (amount.round({R}).amount, currency)']),
        "convert": (f"convert_{n}", [("amount", "MoneyF", "Money", None), ("src", "str", "str", None),
                                     ("dst", "str", "str", None)], ("MoneyF", "Money"),
                    f"The {h} amount converted from ``src`` to ``dst`` at the published rate.",
                    ["if (src, dst) not in RATES:", '    raise KeyError(f"no rate for {src}->{dst}")'],
                    ["return round_money(amount * RATES[(src, dst)], dst)"],
                    ["return Money(amount.amount * RATES[(src, dst)], dst).round({R})"]),
        "quote": (f"quote_{n}", [("amount", "MoneyF", "Money", None), ("src", "str", "str", None),
                                 ("dst", "str", "str", None), ("spread_bp", "int", "int", "25")],
                  ("MoneyF", "Money"),
                  f"A customer {h} quote: the converted amount less a spread in basis points.",
                  ["if (src, dst) not in RATES:", '    raise KeyError(f"no rate for {src}->{dst}")'],
                  ["return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)"],
                  ["return Money(amount.amount * RATES[(src, dst)] * (1 - Decimal(spread_bp) / 10000), dst)"
                   ".round({R})"]),
        "convert_float": ("convert_float", [("amount", "float", "float", None), ("src", "str", "str", None),
                                            ("dst", "str", "str", None)], ("float", "float"),
                          "v1 compatibility shim: float in, float out. legacy/ depends on it; keep its "
                          "signature and results.",
                          [],
                          ["return round(amount * RATES[(src, dst)], EXPONENT[dst])"],
                          ["return round(amount * float(RATES[(src, dst)]), EXPONENT[dst])"]),
        "json_export": ("invoice_json", [("lines", "list", "list", None), ("currency", "str", "str", None)],
                        ("str", "str"),
                        "An invoice as compact JSON: ``lines`` is a list of (sku, amount) pairs.",
                        [],
                        ["total = round_money(sum(a for _, a in lines), currency)",
                         'doc = {"currency": currency,',
                         '       "lines": [{"sku": s, "amount": round_money(a, currency)} for s, a in lines],',
                         '       "total": total}',
                         'return json.dumps(doc, separators=(",", ":"))'],
                        ["total = Money.sum((a for _, a in lines), currency).round({R})",
                         'doc = {"currency": currency,',
                         '       "lines": [{"sku": s, "amount": a.round({R}).to_json()} for s, a in lines],',
                         '       "total": total.to_json()}',
                         'return json.dumps(doc, separators=(",", ":"))']),
        "csv_export": ("ledger_csv", [("rows", "list", "list", None), ("currency", "str", "str", None)],
                       ("str", "str"),
                       "Ledger rows as CSV text: ``rows`` is a list of (date, memo, amount) triples.",
                       [],
                       ['out = ["date,memo,amount,currency\\n"]',
                        "for day, memo, amount in rows:",
                        '    out.append("%s,%s,%.*f,%s\\n" % (day, memo, EXPONENT[currency], amount, currency))',
                        'return "".join(out)'],
                       ['out = ["date,memo,amount,currency\\n"]',
                        "for day, memo, amount in rows:",
                        '    out.append("%s,%s,%s,%s\\n" % (day, memo, amount.round({R}).amount, currency))',
                        'return "".join(out)']),
    }
    return S[kind]


PROSE = [
    "Every figure here ends up on a customer document, so the rounding rules matter more than they look.",
    "The nightly batch and the API share these helpers; keep them free of I/O.",
    "Amounts arrive already validated by the API layer; these functions only check their own preconditions.",
    "Finance reconciles these numbers against the bank file every morning.",
    "Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.",
    "When in doubt about a figure, the ledger is the source of truth, not these helpers.",
    "These functions are pure: same inputs, same outputs, no clock and no database.",
    "Support quotes these numbers to customers, so a cent off is a ticket.",
]


def _ann(a, era):
    return a


def render_function(kind, n, R, era):
    name, params, ret, doc, check, fbody, dbody = func_spec(kind, n)
    sig = []
    for p, fa, da, default in params:
        ann = fa if era == "float" else da
        sig.append(f"{p}: {ann}" + (f" = {default}" if default else ""))
    body = fbody if era == "float" else [x.replace("{R}", R) for x in dbody]
    r = random.Random(f"obench1:money:doc:{name}:{n}")
    lines = [f"def {name}({', '.join(sig)}) -> {ret[0] if era == 'float' else ret[1]}:",
             f'    """{doc}', "", f"    {r.choice(PROSE)}", '    """']
    lines += ["    " + c for c in check]
    lines.append(f'    log.debug("{name} %s", {params[0][0]}!r)'.replace("!r)", ")"))
    lines += ["    " + b for b in body]
    return lines, name


def fillers(n, era):
    cls = "".join(p.capitalize() for p in n.split("_"))
    ann = "MoneyF" if era == "float" else "Money"
    return [
        f"def normalize_{n}_ref(ref: str) -> str:",
        f'    """A {n.replace("_", " ")} reference in canonical form: upper case, single dashes."""',
        '    return "-".join(ref.strip().upper().replace("_", " ").split())',
        "",
        "",
        f"def {n}_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:",
        f'    """When a {n.replace("_", " ")} falls due: ``terms_days`` after issue, moved off weekends."""',
        "    due = issued + datetime.timedelta(days=terms_days)",
        "    while due.weekday() >= 5:",
        "        due += datetime.timedelta(days=1)",
        "    return due",
        "",
        "",
        f"class {cls}Record:",
        f'    """One {n.replace("_", " ")} as the batch jobs pass it around."""',
        "",
        '    __slots__ = ("ref", "amount", "currency")',
        "",
        f"    def __init__(self, ref: str, amount: {ann}, currency: str):",
        f"        self.ref = normalize_{n}_ref(ref)",
        "        self.amount = amount",
        "        self.currency = currency",
        "",
        "    def __repr__(self):",
        f'        return f"{cls}Record({{self.ref!r}}, {{self.amount!r}}, {{self.currency!r}})"',
    ]


def module_src(pkg, mod, R, era):
    n = NOUN[mod]
    title = mod.replace("_", " ")
    r = random.Random(f"obench1:money:mod:{pkg}.{mod}")
    kinds = module_kinds(pkg, mod)
    body, names = [], []
    for k in kinds:
        lines, name = render_function(k, n, R, era)
        body += lines + ["", ""]
        names.append((k, name))
    body += fillers(n, era)
    text = "\n".join(body)

    def uses(word):
        return re.search(r"\b%s\b" % word, text) is not None
    head = [f'"""{pkg.capitalize()}: {title}.', "", " ".join(r.sample(PROSE, 3)), "",
            f"Rounding in this package: {R}." if era == "dec" else
            "Money amounts are floats for now (see MIGRATION.md).", '"""', "import datetime"]
    if uses("json"):
        head.append("import json")
    head.append("import logging")
    if era == "dec":
        dec = [x for x in ("Decimal", R) if uses(x)]
        if dec:
            head.append(f"from decimal import {', '.join(dec)}")
    head.append("")
    if uses("RATES"):
        head.append("from ledgerly._gen.rates_table import RATES")
    if era == "dec":
        head.append("from ledgerly.money import Money")
    else:
        alias = [x for x in ("MoneyF", "Rate") if uses(x)]
        head.append(f"from ledgerly.types import {', '.join(alias)}")
    util = [x for x in ("EXPONENT", "round_money") if uses(x)]
    if util:
        head.append(f"from ledgerly.util import {', '.join(util)}")
    head += ["", "log = logging.getLogger(__name__)", "", ""]
    return "\n".join(head) + "\n" + text + "\n", names


def modules(amended=False, instant=False):
    """[(pkg, mod, R, [(kind, func name)])]"""
    return [(pkg, mod, R, module_src(pkg, mod, R, "float")[1]) for pkg, mod, R in layout(amended, instant)]


# ------------------------------------------------------------- the cases

AM = {c: ["2.675", "1.005", "0.125", "1234.565", "19.995", "0.045", "-2.675", "10.00", "0.005"]
      for c in ("USD", "EUR", "GBP", "CHF")}
AM["JPY"] = ["1234.5", "999.5", "100", "2.5", "-0.5", "0.5"]
AM["KWD"] = ["1.0005", "2.6755", "0.1235", "10.000", "0.0005"]
FACTORS = ["1", "1.5", "0.5", "2.25", "0.1"]
PCTS = ["7.5", "12.5", "0.5", "19.6", "33.3", "10"]


def M(v, c):
    return {"M": [v, c]}


def D(v):
    return {"D": v}


def hidden_cases(kind, fname):
    r = random.Random(f"obench1:money:cases:{fname}")
    curs = list(AM)
    out = []
    for i in range(6):
        c = r.choice(curs)
        a = r.choice(AM[c])
        if kind == "scale":
            out.append([M(a, c), D(r.choice(FACTORS)), c])
        elif kind == "pct":
            out.append([M(a, c), D(r.choice(PCTS)), c])
        elif kind == "total":
            k = i % 4  # one empty list per function
            out.append([{"L": [M(r.choice(AM[c]), c) for _ in range(k)]}, c])
        elif kind == "net":
            out.append([M(a, c), D(r.choice(PCTS)), c])
        elif kind == "cap":
            out.append([M(a, c), D(r.choice(PCTS)), M(r.choice(["0.10", "1.00", "50"]), c), c])
        elif kind == "split":
            amt = {"JPY": ["1000", "100", "7"], "KWD": ["10.000", "1.001"]}.get(c, ["100.00", "10.00", "0.05", "1.00"])
            out.append([M(r.choice(amt), c), r.choice([3, 6, 7]), c])
        elif kind == "accrue":
            out.append([M(r.choice(["1000.00", "2500.50", "999.99", "123456.78"]), "USD"),
                        D(r.choice(["3.5", "7.25", "0.1", "19.99"])), r.choice([30, 31, 365, 1]), "USD"])
        elif kind == "settled":
            b = r.choice([a, str(Decimal(a) + Decimal("0.01")), str(Decimal(a) + Decimal("0.004"))])
            out.append([M(a, c), M(b, c)])
        elif kind == "exceeds":
            out.append([M(a, c), M(r.choice(AM[c]), c)])
        elif kind == "format":
            out.append([M(a, c), c])
        elif kind in ("convert", "quote"):
            src, dst = r.choice(sorted(RATES))
            args = [M(r.choice(AM[src]), src), src, dst]
            out.append(args + ([r.choice([0, 25, 50, 125])] if kind == "quote" else []))
        elif kind == "convert_float":
            src, dst = r.choice(sorted(RATES))
            out.append([float(r.choice(AM[src])), src, dst])
        elif kind == "json_export":
            out.append([{"L": [{"T": [f"SKU-{j}", M(r.choice(AM[c]), c)]} for j in range(i % 3 + 1)]}, c])
        elif kind == "csv_export":
            out.append([{"L": [{"T": [f"2026-10-{j + 1:02d}", f"memo {j}", M(r.choice(AM[c]), c)]}
                               for j in range(i % 3 + 1)]}, c])
    return out


def build(a):
    """Case spec -> plain Decimal values (for expect)."""
    if isinstance(a, dict):
        k, v = next(iter(a.items()))
        if k == "M":
            return ("M", Decimal(v[0]), v[1])
        if k == "D":
            return Decimal(v)
        if k == "L":
            return [build(x) for x in v]
        if k == "T":
            return tuple(build(x) for x in v)
    return a


def expect(kind, args, R):
    """What the Money rendering returns, in normalized form."""
    mode = MODES[R]
    a = [build(x) for x in args]

    def money(v, c):
        return ["M", str(v.normalize()) if v else "0", c]
    if kind == "scale":
        (_, v, c), f, cur = a
        return money(q(v * f, cur, mode), c)
    if kind == "pct":
        (_, v, c), p, cur = a
        return money(q(v * p / 100, cur, mode), c)
    if kind == "total":
        items, cur = a
        return money(q(sum((x[1] for x in items), Decimal(0)), cur, mode), cur)
    if kind == "net":
        (_, v, c), p, cur = a
        return money(v - q(v * p / 100, cur, mode), c)
    if kind == "cap":
        (_, v, c), p, (_, cap, _), cur = a
        return money(min(q(v * p / 100, cur, mode), cap), c)
    if kind == "split":
        (_, v, c), parts, cur = a
        share = q(v / parts, cur, mode)
        return [money(share, c)] * (parts - 1) + [money(q(v - share * (parts - 1), cur, mode), c)]
    if kind == "accrue":
        (_, v, c), rate, days, cur = a
        return money(q(v * rate / 100 * days / 365, cur, mode), c)
    if kind == "settled":
        return a[0][1] == a[1][1]
    if kind == "exceeds":
        return a[0][1] > a[1][1]
    if kind == "format":
        (_, v, c), cur = a
        return "%s %s" % (q(v, cur, mode), cur)
    if kind == "convert":
        (_, v, c), src, dst = a
        return money(q(v * Decimal(RATES[(src, dst)]), dst, mode), dst)
    if kind == "quote":
        (_, v, c), src, dst, bp = a
        return money(q(v * Decimal(RATES[(src, dst)]) * (1 - Decimal(bp) / 10000), dst, mode), dst)
    if kind == "convert_float":
        v, src, dst = a
        return ["F", repr(round(v * float(Decimal(RATES[(src, dst)])), MINOR[dst]))]
    if kind == "json_export":
        lines, cur = a

        def js(x):
            return {"amount": str(q(x, cur, mode)), "currency": cur}
        total = q(sum((x[1][1] for x in lines), Decimal(0)), cur, mode)
        return json.dumps({"currency": cur, "lines": [{"sku": s, "amount": js(m[1])} for s, m in lines],
                           "total": js(total)}, separators=(",", ":"))
    if kind == "csv_export":
        rows, cur = a
        return "date,memo,amount,currency\n" + "".join(
            "%s,%s,%s,%s\n" % (d, memo, q(m[1], cur, mode), cur) for d, memo, m in rows)
    raise KeyError(kind)


def filler_cases(n):
    return [
        (f"normalize_{n}_ref", [["  ab_12 cd "]], "AB-12-CD"),
        (f"normalize_{n}_ref", [["x"]], "X"),
        (f"{n}_due_date", [[{"date": "2026-10-30"}, 1]], "2026-11-02"),
        (f"{n}_due_date", [[{"date": "2026-10-01"}]], "2026-11-02"),  # Oct 31 is a Saturday
        (f"{n}_due_date", [[{"date": "2026-10-02"}, 14]], "2026-10-16"),
    ]


def all_cases(amended=False, instant=False):
    """[{module, func, kind, args, want}] across the codebase."""
    out = []
    for pkg, mod, R, names in modules(amended, instant):
        modpath = f"ledgerly.{pkg}.{mod}"
        for kind, fname in names:
            for args in hidden_cases(kind, fname):
                out.append({"pkg": pkg, "module": modpath, "func": fname, "kind": kind, "args": args,
                            "want": expect(kind, args, R)})
        n = NOUN[mod]
        for fname, argsets, want in filler_cases(n):
            for args in argsets:
                out.append({"pkg": pkg, "module": modpath, "func": fname, "kind": "filler", "args": args,
                            "want": want})
    return out


# ------------------------------------------------------- visible tests

VISIBLE = {
    "scale": ([M("10.00", "USD"), D("1.5"), "USD"], M("15.00", "USD")),
    "pct": ([M("200.00", "USD"), D("7.5"), "USD"], M("15.00", "USD")),
    "total": ([{"L": [M("1.25", "USD"), M("2.50", "USD"), M("3.00", "USD")]}, "USD"], M("6.75", "USD")),
    "net": ([M("200.00", "USD"), D("10"), "USD"], M("180.00", "USD")),
    "cap": ([M("1000.00", "USD"), D("10"), M("50.00", "USD"), "USD"], M("50.00", "USD")),
    "split": ([M("10.00", "USD"), 4, "USD"], {"L": [M("2.50", "USD")] * 4}),
    "accrue": ([M("36500.00", "USD"), D("10"), 1, "USD"], M("10.00", "USD")),
    "settled": ([M("10.00", "USD"), M("10.00", "USD")], True),
    "exceeds": ([M("10.00", "USD"), M("5.00", "USD")], True),
    "format": ([M("2.50", "USD"), "USD"], "2.50 USD"),
    "convert": ([M("100.00", "USD"), "USD", "EUR"], M("92.13", "EUR")),
    "quote": ([M("100.00", "USD"), "USD", "EUR", 50], M("91.67", "EUR")),
    "convert_float": ([100.0, "USD", "EUR"], 92.13),
    "json_export": ([{"L": [{"T": ["A-1", M("10.00", "USD")]}, {"T": ["B-2", M("2.50", "USD")]}]}, "USD"], None),
    "csv_export": ([{"L": [{"T": ["2026-10-01", "rent", M("1200.00", "USD")]}]}, "USD"], None),
}


def lit(a, era):
    if isinstance(a, dict):
        k, v = next(iter(a.items()))
        if k == "M":
            return repr(float(v[0])) if era == "float" else f'Money("{v[0]}", "{v[1]}")'
        if k == "D":
            return repr(float(v)) if era == "float" else f'Decimal("{v}")'
        if k == "L":
            return "[" + ", ".join(lit(x, era) for x in v) + "]"
        if k == "T":
            return "(" + ", ".join(lit(x, era) for x in v) + ("," if len(v) == 1 else "") + ")"
    return repr(a)


def visible_expected(kind, era):
    args, want = VISIBLE[kind]
    if kind == "json_export":
        if era == "float":
            return repr('{"currency":"USD","lines":[{"sku":"A-1","amount":10.0},{"sku":"B-2","amount":2.5}],'
                        '"total":12.5}')
        return repr('{"currency":"USD","lines":[{"sku":"A-1","amount":{"amount":"10.00","currency":"USD"}},'
                    '{"sku":"B-2","amount":{"amount":"2.50","currency":"USD"}}],'
                    '"total":{"amount":"12.50","currency":"USD"}}')
    if kind == "csv_export":
        return repr("date,memo,amount,currency\n2026-10-01,rent,1200.00,USD\n")
    return lit(want, era)


def test_src(pkg, mod, names, era):
    n = NOUN[mod]
    cls = "".join(p.capitalize() for p in f"{pkg}_{mod}".split("_"))
    imports = sorted([f for _, f in names] + [f"normalize_{n}_ref", f"{n}_due_date"])
    out = [f'"""Tests for ledgerly.{pkg}.{mod}."""', "import datetime", "import unittest"]
    if era == "dec":
        out.append("from decimal import Decimal")
        out.append("")
        out.append("from ledgerly.money import Money")
    else:
        out.append("")
    out.append(f"from ledgerly.{pkg}.{mod} import (")
    out += [f"    {x}," for x in imports]
    out += [")", "", "", f"class Test{cls}(unittest.TestCase):"]
    for kind, fname in names:
        args, _ = VISIBLE[kind]
        call = f"{fname}({', '.join(lit(x, era) for x in args)})"
        exp = visible_expected(kind, era)
        out += [f"    def test_{fname}(self):", f"        self.assertEqual({call}, {exp})", ""]
    out += [f"    def test_normalize_{n}_ref(self):",
            f'        self.assertEqual(normalize_{n}_ref("  ab_12 cd "), "AB-12-CD")', "",
            f"    def test_{n}_due_date(self):",
            f"        self.assertEqual({n}_due_date(datetime.date(2026, 10, 30), 1), datetime.date(2026, 11, 2))",
            "", "", 'if __name__ == "__main__":', "    unittest.main()"]
    src = "\n".join(out) + "\n"
    if era == "dec" and 'Decimal("' not in src:
        src = src.replace("from decimal import Decimal\n", "")
    if era == "dec" and "Money(" not in src.split("import (", 1)[1]:
        src = src.replace("\nfrom ledgerly.money import Money\n", "\n")
    return src


# ------------------------------------------------------ fixed files

MONEY_PY = '''"""Money: an exact amount in one currency.

Reviewed and merged in #812. MIGRATION.md moves the rest of ledgerly onto
it; this file itself is done, so please don't change it.
"""
from decimal import Decimal

MINOR_UNITS = {"USD": 2, "EUR": 2, "GBP": 2, "CHF": 2, "JPY": 0, "KWD": 3}


class CurrencyMismatch(ValueError):
    """Arithmetic or comparison across two currencies."""


def _scalar(k):
    if isinstance(k, bool) or isinstance(k, float):
        raise TypeError("Money arithmetic takes int or Decimal, not %s" % type(k).__name__)
    if isinstance(k, int):
        return Decimal(k)
    if isinstance(k, Decimal):
        return k
    return NotImplemented


class Money:
    """An exact amount in one currency. Arithmetic never rounds; call
    ``round(mode)`` where a figure must land on the minor unit."""

    __slots__ = ("amount", "currency")

    def __init__(self, amount, currency):
        if isinstance(amount, (float, bool)):
            raise TypeError("Money takes Decimal, int or str, not %s" % type(amount).__name__)
        if currency not in MINOR_UNITS:
            raise ValueError("unknown currency %r" % (currency,))
        self.amount = amount if isinstance(amount, Decimal) else Decimal(amount)
        self.currency = currency

    @classmethod
    def zero(cls, currency):
        return cls(0, currency)

    @classmethod
    def sum(cls, items, currency):
        """The sum of ``items`` (Money in ``currency``); zero when empty."""
        total = cls.zero(currency)
        for m in items:
            total = total + m
        return total

    def _check(self, other):
        if not isinstance(other, Money):
            return False
        if other.currency != self.currency:
            raise CurrencyMismatch("%s vs %s" % (self.currency, other.currency))
        return True

    def __add__(self, other):
        if not self._check(other):
            return NotImplemented
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        if other == 0 and not isinstance(other, (float, bool)):  # builtin sum() starts at 0
            return self
        return NotImplemented

    def __sub__(self, other):
        if not self._check(other):
            return NotImplemented
        return Money(self.amount - other.amount, self.currency)

    def __neg__(self):
        return Money(-self.amount, self.currency)

    def __abs__(self):
        return Money(abs(self.amount), self.currency)

    def __mul__(self, k):
        k = _scalar(k)
        if k is NotImplemented:
            return NotImplemented
        return Money(self.amount * k, self.currency)

    __rmul__ = __mul__

    def __truediv__(self, k):
        k = _scalar(k)
        if k is NotImplemented:
            return NotImplemented
        return Money(self.amount / k, self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.currency == other.currency and self.amount == other.amount

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __lt__(self, other):
        if not self._check(other):
            return NotImplemented
        return self.amount < other.amount

    def __le__(self, other):
        if not self._check(other):
            return NotImplemented
        return self.amount <= other.amount

    def __gt__(self, other):
        if not self._check(other):
            return NotImplemented
        return self.amount > other.amount

    def __ge__(self, other):
        if not self._check(other):
            return NotImplemented
        return self.amount >= other.amount

    def round(self, rounding):
        """This amount on the currency's minor unit, with ``rounding`` (a
        decimal module constant such as ROUND_HALF_UP)."""
        exp = Decimal(1).scaleb(-MINOR_UNITS[self.currency])
        return Money(self.amount.quantize(exp, rounding=rounding), self.currency)

    def to_json(self):
        """``{"amount": "12.30", "currency": "USD"}``. The amount must
        already be on the minor unit (round it first)."""
        exp = Decimal(1).scaleb(-MINOR_UNITS[self.currency])
        if self.amount != self.amount.quantize(exp):
            raise ValueError("to_json needs a rounded amount, got %s" % self.amount)
        return {"amount": str(self.amount.quantize(exp)), "currency": self.currency}

    def __repr__(self):
        return "Money(%r, %r)" % (str(self.amount), self.currency)

    def __str__(self):
        return "%s %s" % (self.amount, self.currency)
'''

TYPES_FLOAT = '''"""Shared type aliases."""

MoneyF = float  # a money amount as a float; being migrated to ledgerly.money.Money
Rate = float  # a factor, rate or percentage; being migrated to decimal.Decimal
Ref = str  # an external reference
'''
TYPES_DEC = '''"""Shared type aliases."""

Ref = str  # an external reference
'''

UTIL_PY = '''"""Small helpers shared across packages."""

EXPONENT = {"USD": 2, "EUR": 2, "GBP": 2, "CHF": 2, "JPY": 0, "KWD": 3}


def round_money(x: float, currency: str) -> float:
    """A float amount rounded to the currency's minor unit (float era)."""
    return round(x, EXPONENT[currency])
'''

GEN_RATES_FLOAT = '''"""Writes ledgerly/_gen/rates_table.py from data/rates.csv.

Run from the repo root: python3 tools/gen_rates.py
"""
import csv
from pathlib import Path

HEADER = "# GENERATED by tools/gen_rates.py from data/rates.csv; do not edit.\\n"


def main():
    with open("data/rates.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    out = [HEADER, "RATES = {\\n"]
    for r in rows:
        out.append("    (%r, %r): %r,\\n" % (r["src"], r["dst"], float(r["rate"])))
    out.append("}\\n")
    Path("ledgerly/_gen/rates_table.py").write_text("".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
'''
GEN_RATES_DEC = GEN_RATES_FLOAT.replace(
    'out = [HEADER, "RATES = {\\n"]',
    'out = [HEADER, "from decimal import Decimal\\n\\n", "RATES = {\\n"]').replace(
    'out.append("    (%r, %r): %r,\\n" % (r["src"], r["dst"], float(r["rate"])))',
    'out.append("    (%r, %r): Decimal(%r),\\n" % (r["src"], r["dst"], r["rate"]))')
assert GEN_RATES_DEC.count("Decimal") == 2, "gen_rates Money rendering did not apply"


def rates_table(era):
    head = "# GENERATED by tools/gen_rates.py from data/rates.csv; do not edit.\n"
    if era == "float":
        body = "".join("    (%r, %r): %r,\n" % (a, b, float(r)) for (a, b), r in RATES.items())
        return head + "RATES = {\n" + body + "}\n"
    body = "".join("    (%r, %r): Decimal(%r),\n" % (a, b, r) for (a, b), r in RATES.items())
    return head + "from decimal import Decimal\n\nRATES = {\n" + body + "}\n"


LEGACY_PY = '''"""v1 compatibility API. Frozen: ships on the v1 release train, which has
its own review. Don't change anything under legacy/."""
from ledgerly.fx.convert import convert_float


def quote_v1(amount, src, dst):
    """v1 /quote: float amounts on the wire."""
    return {"amount": convert_float(amount, src, dst), "currency": dst}


def batch_quote_v1(amounts, src, dst):
    return [quote_v1(a, src, dst) for a in amounts]
'''


def legacy_test():
    def f(v, s, d):
        return round(v * float(RATES[(s, d)]), MINOR[d])
    return f'''"""v1 API tests. legacy/ is frozen; these must keep passing as they are."""
import unittest

from legacy.v1_api import batch_quote_v1, quote_v1


class TestV1(unittest.TestCase):
    def test_quote(self):
        self.assertEqual(quote_v1(100.0, "USD", "EUR"), {{"amount": {f(100.0, "USD", "EUR")!r}, "currency": "EUR"}})

    def test_quote_jpy(self):
        self.assertEqual(quote_v1(2.675, "USD", "JPY"), {{"amount": {f(2.675, "USD", "JPY")!r}, "currency": "JPY"}})

    def test_batch(self):
        self.assertEqual(batch_quote_v1([1.0, 2.5], "EUR", "GBP"),
                         [{{"amount": {f(1.0, "EUR", "GBP")!r}, "currency": "GBP"}},
                          {{"amount": {f(2.5, "EUR", "GBP")!r}, "currency": "GBP"}}])


if __name__ == "__main__":
    unittest.main()
'''


def rates_test(era):
    if era == "float":
        return '''import unittest

from ledgerly._gen.rates_table import RATES


class TestRates(unittest.TestCase):
    def test_usd_eur(self):
        self.assertEqual(RATES[("USD", "EUR")], 0.9213)

    def test_every_pair(self):
        self.assertEqual(len(RATES), 30)
'''
    return '''import unittest
from decimal import Decimal

from ledgerly._gen.rates_table import RATES


class TestRates(unittest.TestCase):
    def test_usd_eur(self):
        self.assertEqual(RATES[("USD", "EUR")], Decimal("0.92130"))

    def test_every_pair(self):
        self.assertEqual(len(RATES), 30)
'''


def migration_md():
    rows = "\n".join(f"| `ledgerly/{pkg}/` | `{R}` |" for pkg, R, _ in PACKAGES)
    return f"""# Migration: float money → Money

Money amounts in ledgerly are floats. `ledgerly/money.py` adds `Money`, an
exact Decimal amount in one currency (reviewed in #812 — it's done; don't
change it). This migration moves every package onto it.

## Rules

1. Every `MoneyF` annotation becomes `Money`; every `Rate` becomes
   `decimal.Decimal`. When nothing uses them, delete `MoneyF` and `Rate` from
   `ledgerly/types.py`; afterwards nothing under `ledgerly/` or `tests/` may
   mention either name.
2. Keep every function's name and parameter list (names, order, defaults).
   Only the types change. Behaviour stays the same except that the arithmetic
   is exact: where the old code called `round_money`, the new code rounds;
   where it didn't, it doesn't.
3. `round_money(x, currency)` becomes `x.round(<mode>)`, with the rounding
   mode of the package the code lives in:

| package | rounding |
|---|---|
{rows}

4. Comparisons with a tolerance (`abs(a - b) < 0.005`) become exact
   comparisons.
5. Money shown as text (`"%.*f" % ...`) is the Money amount rounded with the
   package's mode — same number of digits as before, but never formatted
   through a float.
6. Sums of Money use `Money.sum(items, currency)`, which is zero for an
   empty list.
7. Exchange rates: `ledgerly/_gen/rates_table.py` is generated by
   `tools/gen_rates.py` from `data/rates.csv`. Don't edit the generated file
   by hand: change the generator so `RATES` maps to `Decimal` values built
   from the CSV text exactly (`Decimal("0.92130")`, never via a float), then
   regenerate.
8. JSON: every money value in exported JSON becomes an object,
   `{{"amount": "12.30", "currency": "USD"}}` (`Money.to_json()`), with the
   amount rounded first.
9. `legacy/` is frozen (the v1 API, on its own release train): don't change
   anything under it. It calls `ledgerly.fx.convert.convert_float`, which
   keeps its float signature and results.
10. Update `tests/` to the new types. Don't drop or skip tests.

The suite: `python3 -m unittest discover -s tests -t .`
"""


def tree(era, amended=False, instant=False):
    """{relative path: text} for the whole repo in one era."""
    files = {
        "README.md": "# ledgerly\n\nBilling, tax, FX and payout arithmetic for the platform.\n\n"
                     "Tests: `python3 -m unittest discover -s tests -t .`\n",
        "MIGRATION.md": migration_md(),
        "ledgerly/__init__.py": '"""ledgerly: money arithmetic for the platform."""\n__version__ = "3.4.0"\n',
        "ledgerly/money.py": MONEY_PY,
        "ledgerly/types.py": TYPES_FLOAT if era == "float" else TYPES_DEC,
        "ledgerly/util.py": UTIL_PY,
        "ledgerly/_gen/__init__.py": "",
        "ledgerly/_gen/rates_table.py": rates_table(era),
        "tools/gen_rates.py": GEN_RATES_FLOAT if era == "float" else GEN_RATES_DEC,
        "data/rates.csv": rates_csv(),
        "legacy/__init__.py": "",
        "legacy/v1_api.py": LEGACY_PY,
        "tests/__init__.py": "",
        "tests/legacy/__init__.py": "",
        "tests/legacy/test_v1.py": legacy_test(),
        "tests/test_rates.py": rates_test(era),
    }
    for pkg, _, _ in PACKAGES:
        files[f"ledgerly/{pkg}/__init__.py"] = f'"""{pkg}: see the modules."""\n'
    for pkg, mod, R in layout(amended, instant):
        if True:
            src, names = module_src(pkg, mod, R, era)
            files[f"ledgerly/{pkg}/{mod}.py"] = src
            files[f"tests/test_{pkg}_{mod}.py"] = test_src(pkg, mod, names, era)
    return files


def visible_count(instant=False):
    return sum(len(names) + 2 for *_, names in modules(instant=instant)) + 2 + 3


SIGNATURES = None


def signatures(instant=False):
    """{(module, func): [[param, default or None], ...]} from the float era."""
    out = {}
    for pkg, mod, R, names in modules(instant=instant):
        m = f"ledgerly.{pkg}.{mod}"
        n = NOUN[mod]
        for kind, fname in names:
            out[f"{m}:{fname}"] = [[p, d] for p, _, _, d in func_spec(kind, n)[1]]
        out[f"{m}:normalize_{n}_ref"] = [["ref", None]]
        out[f"{m}:{n}_due_date"] = [["issued", None], ["terms_days", "30"]]
    return out


AMENDMENT_001 = """# 001 — payouts round half-even

Decided by finance on 2026-10-30, after MIGRATION.md was written.

Payout figures are reconciled against the bank's settlement file, which
rounds half-even. So `ledgerly/payouts/` rounds with `ROUND_HALF_EVEN`, not
`ROUND_HALF_UP` as the table in MIGRATION.md says. This applies to every
module in `ledgerly/payouts/`, including any added later. Everything else in
MIGRATION.md stands.
"""


def write_avalanche_files(root):
    """The files the mountain drops mid-climb (committed in the task dir)."""
    import os
    os.makedirs(os.path.join(root, "avalanche"), exist_ok=True)
    src, names = module_src("payouts", "instant", "ROUND_HALF_UP", "float")
    files = {"avalanche/001-payouts-rounding.md": AMENDMENT_001, "avalanche/instant.py": src,
             "avalanche/test_payouts_instant.py": test_src("payouts", "instant", names, "float")}
    for rel, text in files.items():
        with open(os.path.join(root, rel), "w", encoding="utf-8") as f:
            f.write(text)
