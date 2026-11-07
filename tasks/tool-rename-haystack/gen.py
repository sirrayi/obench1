"""tool-rename-haystack: `harbor`, a ~1,200-file monorepo where
accounts.fetch_user becomes load_account. Every file is rendered from one
plan in a before or after mode (and with or without the mid-climb keyword
addendum), so setup, oracle and grader can't disagree about what a correct
rename touches. The haystack: ten reference forms (star imports, `as`
imports, getattr by name, default arguments, partials, option dicts, mock
targets, route strings, generated code) next to things that only look like
the function (fetch_user_count, prefetch_user, GitHubClient.fetch_user, the
admin shell's own fetch_user, a `fetch_user=` flag, metric names, log text,
vendored copies) and a 30 MB log full of the name."""
import hashlib
import random
import re

PKGS = ["billing", "invoices", "search", "notify", "reports", "export", "sessions", "teams", "orgs", "audit",
        "quotas", "plans", "webhooks", "sso", "profiles", "onboarding", "support", "insights", "jobs", "mail",
        "sms", "push", "imports", "analytics", "feeds", "comments", "uploads", "payments", "ledger", "presence"]
WORDS = ["core", "views", "tasks", "rules", "sync", "digest", "policy", "store", "cache", "events", "hooks", "api",
         "admin", "batch", "cron", "filters", "forms", "models", "queue", "render", "schema", "signals", "stats",
         "util", "worker", "audit_log", "backfill", "limits", "merge", "notes", "owners", "paging", "retry",
         "scoring", "summary", "tags"]
FORMS = ["attr", "direct", "as", "multi", "modalias", "getattr", "star", "default", "partial", "opts"]
BINDS = {"direct", "as", "multi", "star"}
OLD, NEW, OLD_KW, NEW_KW = "fetch_user", "load_account", "include_deleted", "with_deleted"
WARNING = "fetch_user is deprecated, use load_account (removal in 4.0)"
CHANGELOG_LINE = ("- Renamed `accounts.fetch_user` to `accounts.load_account`; "
                  "`fetch_user` is deprecated and goes away in 4.0.")
METRICS = ["accounts.fetch_user.latency", "accounts.fetch_user.errors", "accounts.fetch_user.calls"]
LOG_TEXT = "fetch_user returned nothing for %s"
TEAMMATE = ("harbor/billing/late_fees.py", "tests/test_late_fees.py")
PROTECTED = ("legacy_cache", "third_party")

RENAME = """# Rename: accounts.fetch_user → accounts.load_account (3.2)

`harbor.accounts.fetch_user` becomes `harbor.accounts.load_account`. Same behaviour, new name.

1. Every reference to `harbor.accounts.fetch_user` in harbor/ and tests/ moves to `load_account`: calls,
   imports (`as` imports and star imports included), attribute references, `getattr` by name, `mock.patch`
   targets, and the handler strings in harbor/rpc/routes.py.
2. `fetch_user` stays importable from harbor.accounts for one release, as a wrapper that warns on every call
   and then returns what `load_account` returns:

       warnings.warn("fetch_user is deprecated, use load_account (removal in 4.0)", DeprecationWarning, stacklevel=2)

   It is not in `__all__`; `load_account` takes its place there.
3. Generated code (harbor/proto/*_pb2.py) is never edited by hand: change proto/*.proto and run
   `python3 tools/genproto.py` from the repository root.
4. docs/API.md documents `load_account` (rename its section). Add exactly this line under `## Unreleased` in
   CHANGELOG.md:

       - Renamed `accounts.fetch_user` to `accounts.load_account`; `fetch_user` is deprecated and goes away in 4.0.

5. Leave alone:
   - `fetch_user_count`, and anything else whose name merely contains fetch_user;
   - other things called fetch_user that aren't this function (there are some);
   - strings that aren't a lookup of the function: metric names (`accounts.fetch_user.latency` and friends feed
     dashboards), log and error messages;
   - legacy_cache/ and third_party/ (vendored, byte-compared in CI), and logs/.

   Comments that mention fetch_user may be updated or left. A file that doesn't reference the function
   shouldn't change in any other way.
6. The suite passes: `python3 -m unittest discover -s tests -t .`
"""

ADDENDUM = """# Rename addendum (agreed in review)

While we're in there: `load_account`'s keyword `include_deleted` becomes `with_deleted`.

- Every call site passes `with_deleted` (that includes partials and keyword dicts).
- `load_account` doesn't accept `include_deleted` at all.
- The deprecated `fetch_user` wrapper keeps accepting `include_deleted` and passes it on as `with_deleted`.
- docs/API.md shows the new keyword.
"""


def account(uid, inc):
    deleted = uid % 7 == 0
    if deleted and not inc:
        return None
    return {"id": uid, "name": f"user{uid}", "tier": ("free", "pro", "team")[uid % 3], "deleted": deleted}


def expect(name, kw, uid):
    u = account(uid, kw)
    return f"{name}:none" if u is None else f"{name}:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def plan():
    r = random.Random("obench1:rename")
    mods = []
    for pkg in PKGS:
        for w in WORDS:
            m = {"pkg": pkg, "mod": w, "path": f"harbor/{pkg}/{w}.py", "seed": r.randint(0, 10 ** 9), "funcs": [],
                 "comment": r.random() < 0.12, "metric": r.random() < 0.08, "count": r.random() < 0.06,
                 "prefetch": r.random() < 0.05}
            if r.random() < 0.25:
                forms, bound = [], False
                for _ in range(r.choice([1, 1, 2, 3])):
                    f = r.choice(FORMS)
                    if f in BINDS and bound or f in forms:
                        continue
                    bound |= f in BINDS
                    forms.append(f)
                for f in forms:
                    m["funcs"].append({"name": f"{w}_{f}_owner", "form": f,
                                       "kw": f in ("partial", "opts") or r.random() < 0.4})
                m["logs"] = r.random() < 0.3
            mods.append(m)
    return mods


def callers(mate=False):
    """(module dotted path, function name, kw) for every function the hidden runner calls."""
    out = [(m["path"][:-3].replace("/", "."), f["name"], f["kw"]) for m in plan() for f in m["funcs"]]
    out.append(("harbor.admin.shell", "account_owner", False))
    if mate:
        out += [("harbor.billing.late_fees", "late_fee_owner", True), ("harbor.billing.late_fees", "late_fee_payer", False)]
    return out


def _filler(r, m, n):
    out = []
    for i in range(n):
        k = r.randint(2, 9)
        out += ["", "", f"def {m['mod']}_step_{i}(rows, factor={k}):", f'    """Stage {i} of the {m["pkg"]} pipeline."""',
                "    total = 0", "    for row in rows:", f"        total += row * factor + {r.randint(0, 50)}",
                f"    return total % {r.randint(97, 997)}"]
    return out


def call_expr(f, fn, kw):
    k = f", {kw}=True" if f["kw"] else ""
    return {"attr": f"accounts.{fn}(uid{k})", "direct": f"{fn}(uid{k})", "multi": f"{fn}(uid{k})",
            "star": f"{fn}(uid{k})", "as": f"get_user(uid{k})", "modalias": f"acct.{fn}(uid{k})",
            "getattr": f'getattr(accounts, "{fn}")(uid{k})', "default": f"loader(uid{k})",
            "partial": f"_load_{f['name']}(uid)", "opts": f"accounts.{fn}(uid, **_OPTS_{f['name']})"}[f["form"]]


def module_src(m, after=False, amended=False):
    fn = NEW if after else OLD
    kw = NEW_KW if after and amended else OLD_KW
    r = random.Random(m["seed"])
    forms = {f["form"] for f in m["funcs"]}
    imp = []
    if "partial" in forms:
        imp.append("import functools")
    imp.append("import logging")
    imp.append("")
    if forms & {"attr", "getattr", "default", "partial", "opts"}:
        imp.append("from harbor import accounts")
    if m["metric"]:
        imp.append("from harbor import telemetry")
    if "modalias" in forms:
        imp.append("import harbor.accounts as acct")
    if "direct" in forms:
        imp.append(f"from harbor.accounts import {fn}")
    if "as" in forms:
        imp.append(f"from harbor.accounts import {fn} as get_user")
    if "multi" in forms:
        imp.append(f"from harbor.accounts import (\n    {fn},\n    fetch_user_count,\n)")
    elif m["count"]:
        imp.append("from harbor.accounts import fetch_user_count")
    if "star" in forms:
        imp.append("from harbor.accounts import *  # noqa: F401,F403")
    if imp[-1] == "":
        imp.pop()
    out = [f'"""{m["pkg"]}.{m["mod"]}."""', *imp, "", "log = logging.getLogger(__name__)"]
    for f in m["funcs"]:
        if f["form"] == "partial":
            out.append(f"_load_{f['name']} = functools.partial(accounts.{fn}, {kw}=True)")
        if f["form"] == "opts":
            out.append(f'_OPTS_{f["name"]} = {{"{kw}": True}}')
    if m["comment"]:
        out += ["", f"# {OLD} is cached upstream; don't wrap it in another cache."]
    out += _filler(r, m, r.randint(3, 6))
    for f in m["funcs"]:
        sig = f"uid, loader=accounts.{fn}" if f["form"] == "default" else "uid"
        out += ["", "", f"def {f['name']}({sig}):", f"    u = {call_expr(f, fn, kw)}", "    if u is None:"]
        if m.get("logs"):
            out.append(f'        log.warning("{LOG_TEXT}", uid)')
        out += [f'        return "{f["name"]}:none"', f'    return f"{f["name"]}:{{u[\'name\']}}:{{u[\'tier\']}}:{{int(u[\'deleted\'])}}"']
    if "multi" in forms or m["count"]:
        out += ["", "", f"def {m['mod']}_population():", f"    return fetch_user_count() + {r.randint(1, 99)}"]
    if m["metric"]:
        out += ["", "", f"def {m['mod']}_timer():", f'    return telemetry.timer("{r.choice(METRICS)}")']
    if m["prefetch"]:
        out += ["", "", "def prefetch_user(uid):", '    """Warm the profile cache (not an account lookup)."""', "    return uid"]
    return "\n".join(out) + "\n"


def keep_strings():
    out = []
    for m in plan():
        src = module_src(m)
        out += [(m["path"], s) for s in METRICS + [LOG_TEXT] if f'"{s}"' in src]
    return out


ACCOUNTS_NEW_TAIL = '''

def fetch_user(user_id, *, include_deleted=False):
    """Deprecated: use load_account."""
    warnings.warn("{w}", DeprecationWarning, stacklevel=2)
    return load_account(user_id, {kw}=include_deleted)
'''


def accounts_src(after=False, amended=False):
    fn = NEW if after else OLD
    kw = NEW_KW if after and amended else OLD_KW
    out = ['"""Accounts: the account store."""'] + (["import warnings"] if after else []) + [
        "", f'__all__ = ["{fn}", "fetch_user_count", "account_tiers"]', "", 'TIERS = ("free", "pro", "team")', "", "",
        f"def {fn}(user_id, *, {kw}=False):",
        '    """The account for user_id, or None if it was deleted (unless deleted ones are asked for)."""',
        "    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:",
        '        raise ValueError(f"bad user id: {user_id!r}")', "    deleted = user_id % 7 == 0",
        f"    if deleted and not {kw}:", "        return None",
        '    return {"id": user_id, "name": f"user{user_id}", "tier": TIERS[user_id % 3], "deleted": deleted}', "", "",
        "def fetch_user_count():", '    """How many accounts exist."""', "    return 4242", "", "",
        "def account_tiers():", "    return list(TIERS)"]
    s = "\n".join(out) + "\n"
    return s + ACCOUNTS_NEW_TAIL.format(w=WARNING, kw=kw) if after else s


def proto_src(name, after=False):
    fn = NEW if after else OLD
    rpcs = {"accounts": [("GetUser", f"harbor.accounts:{fn}"), ("CountUsers", "harbor.accounts:fetch_user_count")],
            "billing": [("GetPayer", f"harbor.accounts:{fn}"), ("ListInvoices", "harbor.invoices.store:list_all")],
            "github": [("GetGitHubUser", "harbor.integrations.github:GitHubClient.fetch_user")]}[name]
    out = ['syntax = "proto3";', f"package harbor.{name};", 'import "harbor/options.proto";', "",
           f"service {name.capitalize()} {{"]
    for rpc, h in rpcs:
        out += [f"  rpc {rpc} ({rpc}Request) returns ({rpc}Reply) {{", f'    option (harbor.handler) = "{h}";', "  }"]
    return "\n".join(out + ["}"]) + "\n"


GENPROTO = '''"""Generate harbor/proto/<name>_pb2.py from proto/<name>.proto. Run from the repository root."""
import hashlib
import re
from pathlib import Path

RPC = re.compile(r'rpc\\s+(\\w+)\\s*\\([^)]*\\)\\s*returns\\s*\\([^)]*\\)\\s*\\{\\s*option\\s*\\(harbor\\.handler\\)\\s*=\\s*"([^"]+)";')


def render(src):
    lines = ["# Generated by tools/genproto.py. DO NOT EDIT.",
             "# source-sha256: " + hashlib.sha256(src.encode()).hexdigest(), "", "HANDLERS = {"]
    lines += ['    "%s": "%s",' % m for m in RPC.findall(src)]
    return "\\n".join(lines + ["}", ""])


def main():
    for p in sorted(Path("proto").glob("*.proto")):
        Path("harbor/proto", p.stem + "_pb2.py").write_text(render(p.read_text()))


if __name__ == "__main__":
    main()
'''


def genproto_render(src):
    ns = {}
    exec(compile(GENPROTO, "genproto", "exec"), ns)
    return ns["render"](src)


ROUTES = '''"""RPC routing: route name -> "module:attribute"."""
import importlib

ROUTES = {{
    "user.get": "harbor.accounts:{fn}",
    "user.count": "harbor.accounts:fetch_user_count",
    "user.tiers": "harbor.accounts:account_tiers",
    "github.user": "harbor.integrations.github:GitHubClient.fetch_user",
    "admin.whois": "harbor.admin.shell:whois",
}}


def resolve(name):
    module, _, attr = ROUTES[name].partition(":")
    obj = importlib.import_module(module)
    for part in attr.split("."):
        obj = getattr(obj, part)
    return obj
'''

SHELL = '''"""The admin shell's helpers."""
from harbor import accounts

STAFF = {{"ops@harbor.dev": "ops", "cto@harbor.dev": "cto"}}


def fetch_user(email):
    """Look up a staff member for the admin shell (not an account)."""
    return {{"email": email, "role": STAFF.get(email, "guest")}}


def whois(email):
    return "%s:%s" % (email, fetch_user(email)["role"])


def account_owner(uid):
    u = accounts.{fn}(uid)
    return "account_owner:none" if u is None else "account_owner:%s:%s:%d" % (u["name"], u["tier"], u["deleted"])
'''

GITHUB = '''"""A tiny GitHub client. Nothing to do with harbor accounts."""


class GitHubClient:
    def fetch_user(self, login):
        return {"login": login, "site_admin": login == "octo"}

    def fetch_user_repos(self, login):
        return [login + "/dotfiles"]
'''

SYNC = '''"""Mirror GitHub logins."""
from harbor.integrations.github import GitHubClient


def sync(logins, *, fetch_user=True):
    client = GitHubClient()
    return [client.fetch_user(x)["login"] if fetch_user else x for x in logins]
'''

TEAMMATE_SRC = '''"""Late fees: who owes them, and how many accounts they could apply to."""
from harbor import accounts
from harbor.accounts import fetch_user_count

_OPTS = {{"{kw}": True}}


def late_fee_owner(uid):
    u = accounts.{fn}(uid, **_OPTS)
    if u is None:
        return "late_fee_owner:none"
    return f"late_fee_owner:{{u['name']}}:{{u['tier']}}:{{int(u['deleted'])}}"


def late_fee_payer(uid):
    u = accounts.{fn}(uid)
    if u is None:
        return "late_fee_payer:none"
    return f"late_fee_payer:{{u['name']}}:{{u['tier']}}:{{int(u['deleted'])}}"


def late_fee_population():
    return fetch_user_count()
'''

TEAMMATE_TEST = '''import unittest
from unittest import mock

from harbor.billing import late_fees

MOCK = {{"id": 1, "name": "mocked", "tier": "team", "deleted": False}}


class TestLateFees(unittest.TestCase):
    def test_owner_mocked(self):
        with mock.patch("harbor.accounts.{fn}", return_value=MOCK):
            self.assertEqual(late_fees.late_fee_payer(3), "late_fee_payer:mocked:team:0")

    def test_population(self):
        self.assertEqual(late_fees.late_fee_population(), 4242)
'''


def docs_src(after=False, amended=False):
    fn = NEW if after else OLD
    kw = NEW_KW if after and amended else OLD_KW
    return f"""# harbor API

### accounts.{fn}(user_id, *, {kw}=False)

The account for `user_id` as a dict (`id`, `name`, `tier`, `deleted`), or `None` if the account was deleted and
`{kw}` is false. Raises `ValueError` for ids that aren't positive integers.

### accounts.fetch_user_count()

How many accounts exist.

### accounts.account_tiers()

The tiers, cheapest first.

### integrations.github.GitHubClient.fetch_user(login)

A GitHub user by login. Unrelated to harbor accounts.

### rpc.routes.resolve(name)

The callable behind a route name.
"""


def tests_for(pkg_mods, after=False, amended=False):
    fn = NEW if after else OLD
    pkg = pkg_mods[0]["pkg"]
    picks = [(m, f) for m in pkg_mods for f in m["funcs"]][:4]
    out = ["import unittest", "from unittest import mock", ""]
    out += [f"from harbor.{pkg} import {m}" for m in sorted({m['mod'] for m, _ in picks})]
    out += ["", 'MOCK = {"id": 1, "name": "mocked", "tier": "pro", "deleted": False}', "", "",
            f"class Test{pkg.capitalize()}(unittest.TestCase):"]
    for m, f in picks:
        name, mod = f["name"], m["mod"]
        target = {"attr": f"harbor.accounts.{fn}", "getattr": f"harbor.accounts.{fn}", "opts": f"harbor.accounts.{fn}",
                  "direct": f"harbor.{pkg}.{mod}.{fn}", "multi": f"harbor.{pkg}.{mod}.{fn}",
                  "as": f"harbor.{pkg}.{mod}.get_user"}.get(f["form"])
        if target:
            out += [f"    def test_{name}_mocked(self):", f'        with mock.patch("{target}", return_value=MOCK):',
                    f'            self.assertEqual({mod}.{name}(3), "{name}:mocked:pro:0")', ""]
        out += [f"    def test_{name}(self):", f'        self.assertEqual({mod}.{name}(5), "{expect(name, f["kw"], 5)}")',
                f'        self.assertEqual({mod}.{name}(14), "{expect(name, f["kw"], 14)}")', ""]
    return "\n".join(out).rstrip() + "\n"


def test_accounts_src(after=False, amended=False):
    fn = NEW if after else OLD
    kw = NEW_KW if after and amended else OLD_KW
    s = f'''import unittest

from harbor.accounts import fetch_user_count, {fn}


class TestAccounts(unittest.TestCase):
    def test_get(self):
        self.assertEqual({fn}(5)["name"], "user5")

    def test_deleted_hidden(self):
        self.assertIsNone({fn}(14))

    def test_deleted_on_request(self):
        self.assertTrue({fn}(14, {kw}=True)["deleted"])

    def test_bad_id(self):
        with self.assertRaises(ValueError):
            {fn}(0)

    def test_count(self):
        self.assertEqual(fetch_user_count(), 4242)
'''
    if after:
        s += f'''
    def test_fetch_user_is_deprecated(self):
        from harbor.accounts import fetch_user
        with self.assertWarns(DeprecationWarning):
            self.assertTrue(fetch_user(14, include_deleted=True)["deleted"])
'''
    return s


def tree(after=False, amended=False, mate=False):
    """{path: text} for the whole checkout except logs/."""
    fn = NEW if after else OLD
    kw = NEW_KW if after and amended else OLD_KW
    t = {"README.md": "# harbor\n\nThe harbor monorepo. The current change is described in RENAME.md.\n",
         "RENAME.md": RENAME, ".gitignore": "logs/\n__pycache__/\n*.pyc\n",
         "CHANGELOG.md": "# Changelog\n\n## Unreleased\n\n" + (CHANGELOG_LINE + "\n\n" if after else "")
                         + "## 3.1.0\n\n- Late-fee groundwork in billing.\n- Faster search paging.\n",
         "docs/API.md": docs_src(after, amended), "tools/genproto.py": GENPROTO,
         "harbor/__init__.py": '"""harbor."""\n__version__ = "3.1.0"\n',
         "harbor/accounts/__init__.py": accounts_src(after, amended),
         "harbor/telemetry.py": '"""Metrics."""\n\n\ndef timer(name):\n    return "timer:" + name\n',
         "harbor/rpc/__init__.py": "", "harbor/rpc/routes.py": ROUTES.format(fn=fn),
         "harbor/admin/__init__.py": "", "harbor/admin/shell.py": SHELL.format(fn=fn),
         "harbor/integrations/__init__.py": "", "harbor/integrations/github.py": GITHUB,
         "harbor/integrations/sync.py": SYNC, "harbor/proto/__init__.py": "",
         "tests/__init__.py": "", "tests/test_accounts.py": test_accounts_src(after, amended),
         "tests/test_routes.py": f'''import unittest

from harbor import accounts
from harbor.integrations.github import GitHubClient
from harbor.rpc.routes import resolve


class TestRoutes(unittest.TestCase):
    def test_user_get(self):
        self.assertIs(resolve("user.get"), accounts.{fn})

    def test_github_user(self):
        self.assertIs(resolve("github.user"), GitHubClient.fetch_user)
''',
         "tests/test_integrations.py": '''import unittest

from harbor.admin import shell
from harbor.integrations.sync import sync


class TestIntegrations(unittest.TestCase):
    def test_sync(self):
        self.assertEqual(sync(["octo", "ada"]), ["octo", "ada"])
        self.assertEqual(sync(["x"], fetch_user=False), ["x"])

    def test_whois(self):
        self.assertEqual(shell.whois("ops@harbor.dev"), "ops@harbor.dev:ops")
''',
         "tests/test_proto.py": f'''import unittest
from pathlib import Path

from harbor.proto import accounts_pb2, billing_pb2
from tools.genproto import render


class TestProto(unittest.TestCase):
    def test_handlers(self):
        self.assertEqual(accounts_pb2.HANDLERS["GetUser"], "harbor.accounts:{fn}")
        self.assertEqual(billing_pb2.HANDLERS["GetPayer"], "harbor.accounts:{fn}")

    def test_generated_code_is_fresh(self):
        for p in sorted(Path("proto").glob("*.proto")):
            self.assertEqual(Path("harbor/proto", p.stem + "_pb2.py").read_text(), render(p.read_text()), p.name)
''', "tools/__init__.py": ""}
    for name in ("accounts", "billing", "github"):
        t[f"proto/{name}.proto"] = proto_src(name, after)
        t[f"harbor/proto/{name}_pb2.py"] = genproto_render(proto_src(name, after))
    by_pkg = {}
    for m in plan():
        t[m["path"]] = module_src(m, after, amended)
        by_pkg.setdefault(m["pkg"], []).append(m)
    for pkg, ms in by_pkg.items():
        t[f"harbor/{pkg}/__init__.py"] = ""
        if any(m["funcs"] for m in ms):
            t[f"tests/test_{pkg}.py"] = tests_for([m for m in ms if m["funcs"]], after, amended)
    t["legacy_cache/README.md"] = "Frozen copy of the 2.x accounts client, used by the 2.x migration path.\n"
    t["legacy_cache/__init__.py"] = ""
    t["legacy_cache/accounts_v2.py"] = ('"""2.x accounts client (frozen)."""\n\n\ndef fetch_user(uid):\n'
                                        '    return {"uid": uid, "v": 2}\n')
    t["legacy_cache/migrate.py"] = ('from legacy_cache.accounts_v2 import fetch_user\n\n\ndef migrate(uid):\n'
                                    '    return fetch_user(uid)["uid"]\n')
    t["third_party/ghkit/__init__.py"] = '"""ghkit 0.4.1 (vendored)."""\n'
    t["third_party/ghkit/client.py"] = ('class Client:\n    def fetch_user(self, login):\n'
                                        '        return {"login": login}\n')
    t["third_party/ghkit/LICENSE"] = "MIT License\n\nCopyright (c) ghkit authors\n"
    if mate:
        t[TEAMMATE[0]] = TEAMMATE_SRC.format(fn=fn, kw=kw)
        t[TEAMMATE[1]] = TEAMMATE_TEST.format(fn=fn)
    return t


def rpc_log(f, mb=30):
    r = random.Random("obench1:rename:log")
    routes = [("user.get", f"harbor.accounts:{OLD}"), ("user.count", "harbor.accounts:fetch_user_count"),
              ("github.user", "harbor.integrations.github:GitHubClient.fetch_user"), ("admin.whois", "harbor.admin.shell:whois")]
    size, target, buf = 0, mb << 20, []
    while size < target:
        rt, h = routes[0] if r.random() < 0.7 else r.choice(routes)
        line = (f"2026-10-{r.randint(1, 29):02d}T{r.randint(0, 23):02d}:{r.randint(0, 59):02d}:{r.randint(0, 59):02d}Z "
                f"rpc={rt} handler={h} user={r.randint(1, 99999)} ms={r.randint(1, 900)}\n")
        buf.append(line)
        size += len(line)
        if len(buf) >= 5000:
            f.write("".join(buf))
            buf = []
    f.write("".join(buf))


def log_digest():
    class H:
        def __init__(self):
            self.h = hashlib.sha256()

        def write(self, s):
            self.h.update(s.encode())
    h = H()
    rpc_log(h)
    return h.h.hexdigest()
