"""tool-house-cli: cut a release the way this repo does releases: a project
skill (skills/release/SKILL.md, pointed to by AGENTS.md) driving a house CLI
nobody has seen before (bin/qk), with a stale manual process in the README
as the wrong turn. The signature can only come from the tool."""
import hashlib
import hmac

TASK = "Cut the 2.3.0 release of qk-demo."
KEY = "qk-local-7f3a9e21"
COMMITS = [
    ("feat: add --json output to list", "src/list.py"),
    ("chore: bump dev deps", "requirements-dev.txt"),
    ("fix: handle empty config files", "src/config.py"),
    ("docs: explain the cache dir", "docs/cache.md"),
    ("feat: parallel fetch behind --jobs", "src/fetch.py"),
    ("fix: don't crash on unicode hostnames", "src/net.py"),
    ("test: cover the retry path", "tests/test_retry.py"),
]

QK = r'''#!/usr/bin/env python3
"""qk: the qk-demo house tool. `qk <command> --help` for details."""
import argparse
import hashlib
import hmac
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def log(cmd):
    with open(os.path.join(ROOT, ".qk", "log"), "a") as f:
        f.write(cmd + "\n")


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def version():
    return open(os.path.join(ROOT, "VERSION")).read().strip()


def changelog(a):
    rng = f"{a.since}..HEAD"
    out = git("log", "--reverse", "--format=%h %s", rng)
    if out.returncode:
        sys.exit("qk: unknown ref " + a.since)
    feats, fixes = [], []
    for line in out.stdout.splitlines():
        sha, subj = line.split(" ", 1)
        m = re.match(r"(feat|fix): (.*)", subj)
        if m:
            (feats if m.group(1) == "feat" else fixes).append(f"- {m.group(2)} ({sha})")
    print("### Features\n" + "\n".join(feats) + "\n\n### Fixes\n" + "\n".join(fixes))
    log("changelog " + a.since)


def bump(a):
    cur = [int(x) for x in version().split(".")]
    i = ["major", "minor", "patch"].index(a.part)
    new = cur[:i] + [cur[i] + 1] + [0] * (2 - i)
    new = ".".join(map(str, new))
    if not a.yes:
        sys.stdout.write(f"bump {version()} -> {new}? [y/N] ")
        sys.stdout.flush()
        if sys.stdin.readline().strip().lower() != "y":
            sys.exit("qk: not bumped")
    open(os.path.join(ROOT, "VERSION"), "w").write(new + "\n")
    print(new)
    log("bump " + a.part)


def digest():
    key = open(os.path.join(ROOT, ".qk", "key")).read().strip().encode()
    body = b""
    for name in ("VERSION", "CHANGELOG.md"):
        body += open(os.path.join(ROOT, name), "rb").read()
    return hmac.new(key, body, hashlib.sha256).hexdigest()


def sign(a):
    open(os.path.join(ROOT, "RELEASE.sig"), "w").write(f"qk-sig v1 {version()} {digest()}\n")
    print("signed", version())
    log("sign")


def verify(a):
    st = git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    if st:
        sys.exit("qk: working tree is dirty; commit the release first")
    sig = open(os.path.join(ROOT, "RELEASE.sig")).read().split()
    if sig[2] != version() or sig[3] != digest():
        sys.exit("qk: RELEASE.sig does not match VERSION and CHANGELOG.md")
    print("ok", version())
    log("verify " + git("rev-parse", "HEAD").stdout.strip())


ap = argparse.ArgumentParser(prog="qk")
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("changelog", help="print release notes since a tag")
p.add_argument("--since", required=True)
p.set_defaults(f=changelog)
p = sub.add_parser("bump", help="bump VERSION")
p.add_argument("part", choices=["major", "minor", "patch"])
p.add_argument("--yes", action="store_true", help="don't ask")
p.set_defaults(f=bump)
sub.add_parser("sign", help="write RELEASE.sig for VERSION + CHANGELOG.md").set_defaults(f=sign)
sub.add_parser("verify", help="check RELEASE.sig against a clean, committed tree").set_defaults(f=verify)
a = ap.parse_args()
a.f(a)
'''

FILES = {
    "AGENTS.md": "# Working in qk-demo\n\nProject skills live in `skills/`. Before doing a kind of work that has a skill, read its SKILL.md and follow it; it overrides older docs.\n",
    "skills/release/SKILL.md": """---
name: release
description: Cut a qk-demo release (version bump, changelog, signature, tag).
---

# Releasing qk-demo

Everything goes through `bin/qk`; never edit VERSION or RELEASE.sig by hand.

1. `bin/qk changelog --since v<previous>` prints the notes. Add them to the top of CHANGELOG.md under a `## <new version>` heading, as printed.
2. `bin/qk bump <part>` (minor for a feature release). It asks before writing.
3. `bin/qk sign` writes RELEASE.sig for the new VERSION and CHANGELOG.md.
4. Commit exactly VERSION, CHANGELOG.md and RELEASE.sig, message `release: <version>`.
5. `bin/qk verify` must pass on the committed tree.
6. Tag the release commit: annotated tag `v<version>`, message `qk release <version>`. Don't push; CI picks tags up.
""",
    "README.md": "# qk-demo\n\n## Releasing (old process)\n\nEdit VERSION, add a line to CHANGELOG.md, commit, and `git tag v<version>`.\n",
    "VERSION": "2.2.0\n",
    "CHANGELOG.md": "# Changelog\n\n## 2.2.0\n\n### Features\n- config profiles (1a2b3c4)\n\n### Fixes\n- clearer errors (5d6e7f8)\n",
    "RELEASE.sig": "qk-sig v1 2.2.0 placeholder\n",
    ".qk/key": KEY + "\n",
    ".gitignore": ".qk/log\n__pycache__/\n",
    "bin/qk": QK,
    "src/__init__.py": "",
}


def notes(log_lines):
    """What `qk changelog` prints for `git log --reverse --format='%h %s'` lines."""
    import re
    feats, fixes = [], []
    for line in log_lines:
        sha, subj = line.split(" ", 1)
        m = re.match(r"(feat|fix): (.*)", subj)
        if m:
            (feats if m.group(1) == "feat" else fixes).append(f"- {m.group(2)} ({sha})")
    return "### Features\n" + "\n".join(feats) + "\n\n### Fixes\n" + "\n".join(fixes)


def digest(version_b, changelog_b):
    return hmac.new(KEY.encode(), version_b + changelog_b, hashlib.sha256).hexdigest()
