"""commits.jsonl for if-constraint-gauntlet, and the reference renderer the
grader and oracle share. Every rule in the instruction maps to code here."""
import datetime
import hashlib
import json
import random
import re

HUMANS = ["Ada Okafor", "Bram Visser", "Chen Wei", "Dalia Haddad", "Emil Novak",
          "Farah Siddiqui", "Gus Moreno", "Hana Sato", "Ines Duarte", "Jonas Berg",
          "Kofi Mensah", "Lena Kowalska"]
COAUTHOR_ONLY = "Mira Lindqvist"  # co-authors only: amendment 3 keeps her off the list
BOT = "dependabot[bot]"
SCOPES = ["api", "cli", "core", "db", "ui", "auth", "internal", "deps", None]
TYPES = (["feat"] * 70 + ["fix"] * 80 + ["perf"] * 14 + ["docs"] * 30 + ["chore"] * 40
         + ["refactor"] * 25 + ["test"] * 20 + ["ci"] * 8 + ["build"] * 8 + ["style"] * 5)
VERBS = ["add", "support", "handle", "speed up", "cache", "validate", "expose", "retry",
         "stream", "paginate", "simplify", "harden", "log", "deduplicate", "batch"]
NOUNS = ["user lookups", "session tokens", "the export job", "webhook delivery", "CSV import",
         "rate limits", "search ranking", "invoice totals", "audit events", "schema migrations",
         "config reload", "background jobs", "file uploads", "password resets", "API keys",
         "locale fallbacks", "time zones", "cursor pagination", "health checks", "TLS settings"]
# Old addresses .mailmap folds into the canonical names.
MAILMAP = {"gmoreno@old.example.com": "Gus Moreno", "ada.okafor@old.example.com": "Ada Okafor"}
MAILMAP_TEXT = ("# name canonicalisation\n"
                "Gus Moreno <gus@example.com> <gmoreno@old.example.com>\n"
                "Ada Okafor <ada@example.com> <ada.okafor@old.example.com>\n")
SUBJECT = re.compile(r"^([a-z]+)(?:\(([^()\s]+)\))?(!)?: (\S.*)$")
COAUTHOR = re.compile(r"^Co-authored-by: (.+?) <([^>]+)>$", re.M)
FIXES = re.compile(r"^Fixes #(\d+)$", re.M)


def _hash(i):
    return hashlib.sha1(f"obench1-commit-{i}".encode()).hexdigest()


def _email(name):
    return name.split()[0].lower().strip("[]") + "@example.com"


def commits():
    r = random.Random("obench1:if-constraint-gauntlet")
    base = datetime.datetime(2026, 9, 1, 9, 0, tzinfo=datetime.timezone.utc)
    out = []
    types = TYPES[:]
    r.shuffle(types)
    for i, t in enumerate(types):
        scope = r.choice(SCOPES)
        summary = f"{r.choice(VERBS)} {r.choice(NOUNS)}"
        if r.random() < 0.15:
            summary += "."
        if r.random() < 0.1:
            summary = summary[0].upper() + summary[1:]
        author = r.choice(HUMANS)
        body = []
        if t == "fix" and r.random() < 0.3:
            body += [f"Fixes #{r.randint(10, 999)}" for _ in range(r.randint(1, 2))]
        if r.random() < 0.12:
            co = r.choice([h for h in HUMANS if h != author] + [COAUTHOR_ONLY, "renovate[bot]"])
            body.append(f"Co-authored-by: {co} <{_email(co)}>")
        if scope == "deps" and t in ("fix", "chore") and r.random() < 0.6:
            author, summary = BOT, f"bump {r.choice(['urllib3', 'requests', 'pyyaml'])} from 1.{i} to 1.{i + 1}"
        offset = datetime.timedelta(hours=r.choice([-8, -5, 0, 1, 2, 5.5, 9]))
        when = base + datetime.timedelta(minutes=97 * i + r.randint(0, 50))
        out.append(dict(i=i, type=t, scope=scope, bang=False, summary=summary, author=author,
                        email=_email(author), body=body, when=when, tz=offset, raw=None))

    def plant(k, **kw):
        out[k].update(kw)
    plant(5, type="feat", scope="api", bang=True, summary="drop the v1 /users endpoint", body=[])
    plant(17, type="fix", scope=None, bang=True, summary="reject unsigned webhooks",
          body=["Fixes #77", "Fixes #78"])
    plant(29, type="refactor", scope="core", bang=True, summary="rename Settings to Config", body=[])
    plant(41, type="chore", scope="internal", bang=True, summary="require Python 3.11", body=[])
    plant(53, type="feat", scope="deps", bang=True, summary="move to pydantic 3", body=[])
    plant(66, type="docs", scope="cli", bang=True, summary="the --legacy flag is gone", body=[])
    plant(71, type="feat", scope="db", summary="add read replicas",
          body=["BREAKING CHANGE: replica lag is now visible to readers"])
    plant(88, type="fix", scope="ui", summary='don\'t crash on "!" input', body=[])
    plant(90, type="feat", scope="internal", summary="new metrics plumbing", body=[])
    plant(91, type="fix", scope="internal", summary="flaky lock in tests", body=["Fixes #300"])
    plant(100, type="fix", scope="db", summary="handle null owner.", body=["Fixes #12"],
          author="Chen Wei", email=_email("Chen Wei"))
    plant(140, type="fix", scope="db", summary="Handle null owner", body=["Fixes #40", "Fixes #12"],
          author="Gus Moreno", email=_email("Gus Moreno"))
    plant(110, type="feat", scope="cli", summary="add --json output", body=[], author="Hana Sato",
          email=_email("Hana Sato"))
    plant(150, type="feat", scope="cli", summary="add --json output.", body=[], author="Hana Sato",
          email=_email("Hana Sato"))
    plant(190, type="feat", scope="cli", summary="Add --json output", body=[], author="Ines Duarte",
          email=_email("Ines Duarte"))
    plant(120, type="fix", scope="api", summary="handle timeouts", body=["Closes #55", "Fixes #56",
                                                                        "fixes #57", "Fixes #58 and #59"])
    plant(121, type="fix", scope="cli", summary="handle timeouts", body=[])
    plant(130, type="feat", scope="auth", summary="sessions survive restarts", body=["Fixes #5"])
    plant(160, type="feat", scope="ui", summary=("render every column of the account overview "
                                                 "table with consistent widths, padding and wrapping "
                                                 "across all supported locales"), body=[])
    plant(170, type="fix", scope="api", summary=("return a precise error when the upstream identity "
                                                 "provider rejects the client assertion during refresh"),
          body=["Fixes #612"])
    plant(175, type="perf", scope="search", summary="cache tokenizer tables", body=[])
    plant(176, type="perf", scope=None, summary="avoid a copy in the export path", body=[])
    plant(180, type="feat", scope="api", summary="webhook signatures", body=[],
          author="Kofi Mensah", email=_email("Kofi Mensah"))
    plant(181, type="feat", scope="ui", summary="dark mode", author="Lena Kowalska",
          email=_email("Lena Kowalska"),
          body=[f"Co-authored-by: {COAUTHOR_ONLY} <mira@example.com>",
                "Co-authored-by: Kofi Mensah <kofi@example.com>",
                "Co-authored-by: Ada O. <ada.okafor@old.example.com>"])
    plant(200, type="fix", scope="core", summary="close file handles", body=[])
    plant(201, type="perf", scope="db", summary="batch inserts", body=[])
    plant(202, type="feat", scope="cli", summary="shell completion", body=[])
    plant(203, type="fix", scope="deps", summary="pin certifi", body=[], author="Jonas Berg",
          email=_email("Jonas Berg"))
    # A pair whose local timestamps sort the wrong way as strings: 206 is
    # the later instant (01:00Z) but reads 20:00-05:00 on the previous day.
    plant(205, type="feat", scope="core", summary="plugin hooks", body=[],
          when=datetime.datetime(2026, 10, 2, 23, 0, tzinfo=datetime.timezone.utc),
          tz=datetime.timedelta(hours=9))
    plant(206, type="feat", scope="core", summary="plugin registry", body=[],
          when=datetime.datetime(2026, 10, 3, 1, 0, tzinfo=datetime.timezone.utc),
          tz=datetime.timedelta(hours=-5))
    # Headers that aren't conventional, and a squash whose body only looks like one.
    plant(220, raw="Feat: add tracing", body=[])
    plant(221, raw="fix(api):missing space after the colon", body=[])
    plant(222, raw="fix (cli): stray space before the scope", body=[])
    plant(223, raw="chore: squash merge of #431",
          body=["* feat(api): bulk export", "* fix(api): export crash on empty sets"])
    # Old addresses that .mailmap canonicalises.
    for k in (30, 60, 95, 125, 155, 185):
        out[k].update(author="gus", email="gmoreno@old.example.com")
    for c in out:
        if c["raw"] is None:
            scope = f"({c['scope']})" if c["scope"] else ""
            c["subject"] = f"{c['type']}{scope}{'!' if c['bang'] else ''}: {c['summary']}"
        else:
            c["subject"] = c["raw"]
    reverts = [(212, 200), (213, 201), (214, 202), (215, None)]
    for k, target in reverts:
        if target is None:
            subj, h = "fix(api): an old fix from 4.0", _hash(9999)
        else:
            subj, h = out[target]["subject"], _hash(target)
        out[k].update(subject=f'Revert "{subj}"', body=[f"This reverts commit {h}."])
    rows = []
    for c in out:
        tz = datetime.timezone(c["tz"])
        msg = c["subject"] + ("\n\n" + "\n".join(c["body"]) if c["body"] else "")
        rows.append({"hash": _hash(c["i"]), "author": c["author"], "email": c["email"],
                     "date": c["when"].astimezone(tz).isoformat(), "message": msg})
    r.shuffle(rows)  # the file isn't in date order either
    return rows


def norm(summary):
    s = summary[:1].upper() + summary[1:]
    return s[:-1] if s.endswith(".") else s


def canon(name, email):
    return MAILMAP.get(email, name)


def render(rows):
    reverted, reverts = set(), set()
    for c in rows:
        subj = c["message"].split("\n", 1)[0]
        if subj.startswith('Revert "'):
            reverts.add(c["hash"])
            m = re.search(r"This reverts commit ([0-9a-f]{40})\.", c["message"])
            if m:
                reverted.add(m.group(1))
    sections = {"Breaking changes": [], "Features": [], "Fixes": []}
    kept = []
    for c in rows:
        if c["hash"] in reverted or c["hash"] in reverts:
            continue
        subj, _, body = c["message"].partition("\n")
        m = SUBJECT.match(subj)
        if not m:
            continue
        typ, scope, bang, summary = m.groups()
        if bang:
            sec = "Breaking changes"
        elif typ in ("feat", "perf"):
            sec = "Features"
        elif typ == "fix":
            sec = "Fixes"
        else:
            continue
        if scope == "internal" and not bang:
            continue
        scope = scope or "general"
        if scope == "deps":
            scope = "dependencies"
        s = norm(summary)
        if typ == "perf":
            s += " [perf]"
        refs = FIXES.findall(body) if typ == "fix" else []
        when = datetime.datetime.fromisoformat(c["date"])
        sections[sec].append(dict(scope=scope, summary=s, refs=refs, when=when, c=c))
        kept.append(c)
    lines = ["# Release 4.2.0", ""]
    for sec, entries in sections.items():
        if not entries:
            continue
        groups = {}
        for e in sorted(entries, key=lambda e: e["when"], reverse=True):
            groups.setdefault((e["scope"], e["summary"]), []).append(e)
        merged = sorted(groups.values(), key=lambda g: (g[0]["scope"], -g[0]["when"].timestamp()))
        lines += [f"## {sec}", ""]
        for g in merged:
            refs = []
            for e in g:
                for x in e["refs"]:
                    if x not in refs:
                        refs.append(x)
            tail = "".join(f" (#{x})" for x in refs) + " (" + ", ".join(e["c"]["hash"][:7] for e in g) + ")"
            head = f"- **{g[0]['scope']}:** "
            summary = g[0]["summary"]
            if len(head + summary + tail) > 100:
                summary = summary[: 100 - len(head) - len(tail) - 1].rstrip() + "…"
            lines.append(head + summary + tail)
        lines.append("")
    credit, authored = {}, set()
    for c in kept:
        author = canon(c["author"], c["email"])
        names = {author} | {canon(n, e) for n, e in COAUTHOR.findall(c["message"])}
        authored.add(author)
        for n in names:
            credit[n] = credit.get(n, 0) + 1
    people = [n for n in credit if n in authored and not n.endswith("[bot]")]
    lines += ["## Contributors", ""]
    for n in sorted(people, key=lambda n: (-credit[n], n)):
        lines.append(f"- {n} ({credit[n]})")
    return "\n".join(lines) + "\n"


def jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
