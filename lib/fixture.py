"""Setup helpers: deterministic files and git history. Python 3.9 stdlib."""

import os
import random
import subprocess
from pathlib import Path

WS = Path(os.environ.get("OBENCH_WS", "."))
GIT_ENV = {
    "GIT_AUTHOR_NAME": "Dana Reyes", "GIT_AUTHOR_EMAIL": "dana@example.com",
    "GIT_COMMITTER_NAME": "Dana Reyes", "GIT_COMMITTER_EMAIL": "dana@example.com",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def write(rel, text, mode=None, newline=None):
    p = WS / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        p.write_bytes(text)
    else:
        with open(p, "w", encoding="utf-8", newline=newline or "") as f:
            f.write(text)
    if mode is not None:
        os.chmod(p, mode)
    return p


def sh(cmd, env=None, check=True, cwd=None, input=None):
    e = dict(os.environ)
    e.update(GIT_ENV)
    e.update(env or {})
    p = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd or WS, env=e,
                       capture_output=True, text=True, input=input)
    if check and p.returncode != 0:
        raise SystemExit(f"setup command failed: {cmd}\n{p.stdout}\n{p.stderr}")
    return p.stdout


def git_init(branch="main"):
    sh(["git", "init", "-q", "-b", branch])
    sh(["git", "config", "user.name", "Dana Reyes"])
    sh(["git", "config", "user.email", "dana@example.com"])
    sh(["git", "config", "commit.gpgsign", "false"])
    sh(["git", "config", "core.autocrlf", "false"])


_clock = [1_790_000_000]


def commit(msg, author=None, when=None, add="-A"):
    _clock[0] += 3600
    t = when or _clock[0]
    env = {"GIT_AUTHOR_DATE": f"{t} +0000", "GIT_COMMITTER_DATE": f"{t} +0000"}
    if author:
        name, email = author
        env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email)
    if add:
        sh(["git", "add", add])
    sh(["git", "commit", "-q", "--allow-empty", "-m", msg], env=env)
    return sh(["git", "rev-parse", "HEAD"]).strip()


def rng(name):
    """A per-purpose RNG: same workspace for every harness and seed."""
    return random.Random(f"obench1:{name}")
