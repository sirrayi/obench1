"""The jail every harness runs in during an agent cell.

The runner sets PROFILE to a sandbox-exec profile that denies the harness,
and everything it starts, any read or write of the benchmark folder, the
cells' private dirs and other places that hold answers. It travels as a
module global, never through the environment, so the harness can't read
which paths it hides."""

PROFILE = None


def wrap(cmd):
    return ["/usr/bin/sandbox-exec", "-p", PROFILE, *cmd] if PROFILE else list(cmd)
