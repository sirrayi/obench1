"""orch-spec-audit-24: 24 services, a 15-clause spec (+C16 mid-climb), and
the reference checker. The generator plants violations and look-alikes;
`check()` reads files exactly as the spec words them, and the generator
asserts the two agree, so the ground truth can't drift from the files."""
import ast
import hashlib
import json
import random
import re

N = 24
TEAMS = ["payments", "search", "identity", "growth", "infra", "data", "mobile", "support"]
LFS = {"svc-11", "svc-19"}
FIXED_BY_TEAMMATE = "svc-07"  # gets C4 and C13; a teammate fixes its config mid-climb
CLAUSES = [f"C{i}" for i in range(1, 16)]
LFS_HEAD = "version https://git-lfs.github.com/spec/v1"

SPEC = """# Service baseline spec, rev 7

Every service under services/ must meet these clauses. Each is checked
exactly as written.

- **C1** Public services (`"exposure": "public"` in config.json) set `timeout_s` to 30 or less.
- **C2** Every function in src/handlers.py whose name starts with `handle_` has a docstring.
- **C3** No call to `print(...)` in any .py file under src/. Comments, string contents and methods
  that happen to be called print (`x.print(...)`) don't count.
- **C4** `retries` in config.json is an integer from 1 to 5.
- **C5** Every `FROM` line in the Dockerfile pins its image by digest: `@sha256:` followed by exactly
  64 lowercase hex characters.
- **C6** The Dockerfile's last `USER` line exists and names neither `root` nor `0`.
- **C7** README.md has a line that is exactly `## Runbook`.
- **C8** CODEOWNERS has a `*` rule whose owner is `@team-<team>`, with `<team>` from config.json.
- **C9** No string literal in a .py file under src/ starts with `sk_live_` or `AKIA`. Files outside
  src/ (tests, docs) don't count, and neither do comments.
- **C10** config.json sets `healthcheck`, and src/handlers.py defines `handle_<last path segment>`
  (`/healthz` → `handle_healthz`).
- **C11** `metrics_port` differs from `port`.
- **C12** Every line of requirements.txt that isn't blank or a `#` comment pins an exact version
  with `==`.
- **C13** `log_level` isn't `DEBUG`.
- **C14** Public services set `max_body_kb` to 1024 or less.
- **C15** tests/ contains at least one file named `test_*.py`.

## Services we can't check

Some services keep their sources in Git LFS, and this checkout doesn't have the objects: those files
are LFS pointers (their first line is `version https://git-lfs.github.com/spec/v1`). If any file of a
service is a pointer, the service is **unverifiable**: report that, with no violations. Don't guess.

## Report

One file per service, `findings/svc-XX.json`:

    {"service": "svc-07", "status": "violations", "violations": ["C4", "C13"]}

`status` is `compliant` (no violations), `violations`, or `unverifiable`. `violations` lists clause
ids in clause order. Don't change anything under services/.
"""

AMENDMENT = """# Spec amendment 1 (rev 8)

Adds one clause, effective immediately, for every service:

- **C16** Public services set `rate_limit_rps` in config.json to an integer from 1 to 10000.

Everything else in rev 7 stands. Reports must cover C16 too.
"""


def _filler(r, svc):
    """Several hundred lines of ordinary helper code per service."""
    out = ['"""Helpers for ' + svc + '."""', "import logging", "", "log = logging.getLogger(__name__)", ""]
    for i in range(r.randint(40, 55)):
        k = r.randint(2, 9)
        out += ["", f"def helper_{i}(values, factor={k}):",
                f'    """Scale and clip a batch for stage {i}."""',
                "    out = []", "    for v in values:",
                f"        v = v * factor + {r.randint(0, 99)}",
                f"        if v > {r.randint(100, 999)}:", "            log.info(\"clipped %s\", v)",
                f"            v = {r.randint(100, 999)}", "        out.append(v)", "    return out"]
    return "\n".join(out) + "\n"


def plan():
    """{svc: {"viol": set, "decoys": set, "cfg": {...}, ...}} — what each service is."""
    r = random.Random("obench1:audit24")
    out = {}
    for i in range(1, N + 1):
        svc = f"svc-{i:02d}"
        exposure = "public" if r.random() < 0.6 else "internal"
        viol = {c for c in CLAUSES if r.random() < 0.17}
        if exposure != "public":
            viol -= {"C1", "C14"}
        if svc == FIXED_BY_TEAMMATE:
            exposure = "public"
            viol |= {"C4", "C13"}
        decoys = {d for d in ["print_comment", "print_attr", "print_string", "user_switch", "timeout_edge",
                              "secret_tests", "secret_comment", "req_comment", "body_edge",
                              "internal_limits"] if r.random() < 0.4}
        out[svc] = {"svc": svc, "team": r.choice(TEAMS), "exposure": exposure, "viol": viol, "decoys": decoys,
                    "port": r.choice([8000, 8080, 9000]), "seed": r.randint(0, 10 ** 9),
                    "rps": None if (exposure == "public" and r.random() < 0.35) else r.randint(50, 5000)}
    return out


def files(p, teammate_fixed=False):
    """{relative path under services/<svc>/: text}"""
    r = random.Random(p["seed"])
    v, d = set(p["viol"]), p["decoys"]
    port = p["port"]
    cfg = {"name": p["svc"], "team": p["team"], "exposure": p["exposure"], "port": port,
           "metrics_port": port if "C11" in v else port + 1,
           "timeout_s": (r.choice([45, 60, 120]) if "C1" in v else (30 if "timeout_edge" in d else r.choice([5, 10, 15]))),
           "retries": r.choice([0, 7, 12]) if "C4" in v else r.randint(1, 5),
           "log_level": "DEBUG" if "C13" in v else r.choice(["INFO", "WARNING"]),
           "max_body_kb": r.choice([2048, 4096]) if "C14" in v else (1024 if "body_edge" in d else 512)}
    if teammate_fixed and p["svc"] == FIXED_BY_TEAMMATE:  # after the draws, so nothing else moves
        cfg["retries"], cfg["log_level"] = 2, "INFO"
    if "internal_limits" in d and p["exposure"] == "internal":
        cfg["timeout_s"], cfg["max_body_kb"] = 90, 8192  # C1 and C14 are for public services only
    if "C10" in v and r.random() < 0.5:
        health = None
    else:
        health = r.choice(["/healthz", "/livez", "/ready"])
    if health:
        cfg["healthcheck"] = health
    if p["exposure"] == "public" and p["rps"] is None:
        pass  # no rate_limit_rps: a C16 violation once the amendment lands
    elif p["rps"] is not None:
        cfg["rate_limit_rps"] = p["rps"]
    if p["exposure"] == "internal" and p["rps"] is None:
        cfg["rate_limit_rps"] = 100
    digest = hashlib.sha256(p["svc"].encode()).hexdigest()
    lines = []
    if "C5" in v:
        lines.append(r.choice(["FROM python:3.12-slim", f"FROM python:3.12-slim@sha256:{digest[:63]}"]))
    else:
        lines.append(f"FROM python:3.12-slim@sha256:{digest}")
    lines += ["WORKDIR /app", "COPY requirements.txt .", "RUN pip install --no-cache-dir -r requirements.txt"]
    if "user_switch" in d and "C6" not in v:
        lines += ["USER root", "RUN apt-get update && apt-get install -y curl", "USER app"]
    elif "C6" in v:
        lines += r.choice([[], ["USER root"], ["USER 0"]])
    else:
        lines += ["USER app"]
    lines += ["COPY src/ src/", f"EXPOSE {port}", 'CMD ["python", "-m", "src.app"]']
    dockerfile = "\n".join(lines) + "\n"
    readme = [f"# {p['svc']}", "", f"Owned by the {p['team']} team.", ""]
    readme += (["## Run book", "", "Page the on-call."] if "C7" in v and r.random() < 0.5 else
               (["## Notes", "", "Page the on-call."] if "C7" in v else ["## Runbook", "", "Page the on-call."]))
    owner = (f"@team-{p['team']}s" if r.random() < 0.5 else "@platform") if "C8" in v else f"@team-{p['team']}"
    codeowners = f"# owners\n* {owner}\n/docs/ @docs-team\n"
    req = ["# runtime", "requests==2.32.3", "pydantic==2.9.2"]
    if "req_comment" in d:
        req.append("# urllib3 is pinned by requests")
    req.append("structlog>=24.1" if "C12" in v else "structlog==24.4.0")
    handlers = ['"""HTTP handlers."""', "import json", "import logging", "", "log = logging.getLogger(__name__)", ""]
    names = ["handle_create", "handle_get", "handle_list", "handle_delete"]
    if health:
        hname = "handle_" + health.rsplit("/", 1)[1]
        if "C10" in v:
            hname = "handle_health_check"
        names.append(hname)
    nodoc = r.choice(names) if "C2" in v else None
    for n in names:
        handlers += ["", "", f"def {n}(request):"]
        if n != nodoc:
            handlers.append(f'    """{n.replace("handle_", "").capitalize()} endpoint."""')
        handlers += ['    log.info("%s", request.get("path"))', '    return {"status": 200, "body": json.dumps({"ok": True})}']
    if "print_comment" in d:
        handlers += ["", "", "# print(request) was here while debugging; use log instead"]
    if "print_string" in d:
        handlers += ["", "", 'HELP = "never print( a request body; it may hold personal data"']
    app = ['"""Entry point."""', "import logging", "", "from src import handlers  # noqa: F401", "",
           "log = logging.getLogger(__name__)", "", "", "class Reporter:", "    def __init__(self, printer):",
           "        self.printer = printer", "", "    def report(self, rows):"]
    app.append("        self.printer.print(rows)" if "print_attr" in d else "        log.info(\"%d rows\", len(rows))")
    app += ["", "", "def main():", '    log.info("starting")']
    if "C3" in v:
        app.append('    print("starting on port", ' + str(port) + ")")
    app += ["", "", 'if __name__ == "__main__":', "    main()"]
    util = _filler(r, p["svc"])
    if "C9" in v:
        util += "\nSTRIPE_KEY = " + repr(r.choice(["sk_live_", "AKIA"]) + hashlib.md5(p["svc"].encode()).hexdigest()[:16]) + "\n"
    if "secret_comment" in d:
        util += "\n# keys like sk_live_... come from the vault, never from code\n"
    out = {"config.json": json.dumps(cfg, indent=2) + "\n", "Dockerfile": dockerfile, "README.md": "\n".join(readme) + "\n",
           "CODEOWNERS": codeowners, "requirements.txt": "\n".join(req) + "\n",
           "src/__init__.py": "", "src/handlers.py": "\n".join(handlers) + "\n", "src/app.py": "\n".join(app) + "\n",
           "src/util.py": util}
    if "C15" not in v:
        out["tests/test_handlers.py"] = "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n"
    else:
        out["tests/README.md"] = "Tests live in the monorepo's integration suite.\n"
    if "secret_tests" in d:
        out["tests/fixtures.py"] = 'FAKE_KEY = "sk_live_' + "0" * 16 + '"  # a fixture, never a real key\n'
    if p["svc"] in LFS:
        for f in ("src/handlers.py", "src/app.py"):
            oid = hashlib.sha256((p["svc"] + f).encode()).hexdigest()
            out[f] = f"{LFS_HEAD}\noid sha256:{oid}\nsize {r.randint(2000, 9000)}\n"
    return out


# ----------------------------------------------------------- the checker

def check(fs, amended=False):
    """(status, [clause ids]) for one service's files, exactly per the spec."""
    if any(t.split("\n", 1)[0].strip() == LFS_HEAD for t in fs.values()):
        return "unverifiable", []
    cfg = json.loads(fs["config.json"])
    pub = cfg.get("exposure") == "public"
    v = []
    if pub and not (isinstance(cfg.get("timeout_s"), int) and cfg["timeout_s"] <= 30):
        v.append("C1")
    tree = ast.parse(fs.get("src/handlers.py", ""))
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if any(f.name.startswith("handle_") and ast.get_docstring(f) is None for f in fns):
        v.append("C2")
    printed, secret = False, False
    for path, text in fs.items():
        if path.startswith("src/") and path.endswith(".py"):
            for node in ast.walk(ast.parse(text)):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                    printed = True
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and \
                        node.value.startswith(("sk_live_", "AKIA")):
                    secret = True
    if printed:
        v.append("C3")
    rt = cfg.get("retries")
    if not (isinstance(rt, int) and not isinstance(rt, bool) and 1 <= rt <= 5):
        v.append("C4")
    df = fs.get("Dockerfile", "").splitlines()
    froms = [x for x in df if x.strip().upper().startswith("FROM ")]
    if not froms or not all(re.search(r"@sha256:[0-9a-f]{64}(\s|$)", x) for x in froms):
        v.append("C5")
    users = [x.split(None, 1)[1].strip() if len(x.split()) > 1 else "" for x in df if x.strip().upper().startswith("USER")]
    if not users or users[-1] in ("root", "0"):
        v.append("C6")
    if "## Runbook" not in fs.get("README.md", "").splitlines():
        v.append("C7")
    rules = [x.split() for x in fs.get("CODEOWNERS", "").splitlines() if x.strip() and not x.startswith("#")]
    if not any(r_[0] == "*" and f"@team-{cfg.get('team')}" in r_[1:] for r_ in rules):
        v.append("C8")
    if secret:
        v.append("C9")
    h = cfg.get("healthcheck")
    if not h or not any(f.name == "handle_" + h.rstrip("/").rsplit("/", 1)[-1] for f in fns):
        v.append("C10")
    if cfg.get("metrics_port") == cfg.get("port"):
        v.append("C11")
    reqs = [x.strip() for x in fs.get("requirements.txt", "").splitlines() if x.strip() and not x.strip().startswith("#")]
    if not all(re.match(r"^[A-Za-z0-9_.\-\[\]]+==[^=\s]+(\s+#.*)?$", x) for x in reqs):
        v.append("C12")
    if cfg.get("log_level") == "DEBUG":
        v.append("C13")
    if pub and not (isinstance(cfg.get("max_body_kb"), int) and cfg["max_body_kb"] <= 1024):
        v.append("C14")
    if not any(re.match(r"^tests/test_[^/]*\.py$", p) for p in fs):
        v.append("C15")
    if amended and pub:
        rps = cfg.get("rate_limit_rps")
        if not (isinstance(rps, int) and not isinstance(rps, bool) and 1 <= rps <= 10000):
            v.append("C16")
    return ("violations" if v else "compliant"), v


def truth(amended=False, teammate_fixed=False):
    return {svc: check(files(p, teammate_fixed), amended) for svc, p in plan().items()}


def self_check():
    for svc, p in plan().items():
        st, v = check(files(p))
        if svc in LFS:
            assert st == "unverifiable", svc
        else:
            assert set(v) == p["viol"], (svc, sorted(p["viol"]), v)
