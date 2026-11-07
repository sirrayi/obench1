"""Find and kill processes a cell left behind: any process whose working
directory or command line sits inside the cell's workspace. macOS `ps` and
`lsof`; Python 3.9 stdlib."""

import os
import signal
import subprocess
import time


def find(marker):
    """[(pid, command)] for processes tied to `marker` (a workspace path)."""
    marker = os.path.realpath(marker)
    hits = {}
    try:
        ps = subprocess.run(["ps", "-axww", "-o", "pid=,command="], capture_output=True,
                            text=True, timeout=20, cwd="/").stdout
    except (OSError, subprocess.TimeoutExpired):
        ps = ""
    cmds = {}
    for line in ps.splitlines():
        line = line.strip()
        if not line:
            continue
        pid, _, cmd = line.partition(" ")
        try:
            pid = int(pid)
        except ValueError:
            continue
        cmds[pid] = cmd
        if marker in cmd or marker.replace("/private/var/", "/var/") in cmd:
            hits[pid] = cmd
    try:
        lsof = subprocess.run(["lsof", "-a", "-d", "cwd", "-F", "pn"], capture_output=True,
                              text=True, timeout=30, cwd="/").stdout
    except (OSError, subprocess.TimeoutExpired):
        lsof = ""
    pid = None
    for line in lsof.splitlines():
        if line.startswith("p"):
            try:
                pid = int(line[1:])
            except ValueError:
                pid = None
        elif line.startswith("n") and pid is not None:
            path = os.path.realpath(line[1:])
            if path == marker or path.startswith(marker + os.sep):
                hits[pid] = cmds.get(pid, "?")
    hits.pop(os.getpid(), None)
    return sorted(hits.items())


def kill(marker, grace=2.0):
    """SIGTERM then SIGKILL everything tied to `marker`. Returns what was found."""
    found = find(marker)
    for pid, _ in found:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
    if found:
        time.sleep(grace)
        for pid, _ in find(marker):
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
    return found


if __name__ == "__main__":
    import sys
    for p, c in (kill if "--kill" in sys.argv else find)(sys.argv[1]):
        print(p, c)
