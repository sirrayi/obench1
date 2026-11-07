"""Copy a directory tree, skipping files that are already up to date."""
import argparse
import os
import shutil


def plan(src, dst):
    for d, _, files in os.walk(src):
        for f in sorted(files):
            s = os.path.join(d, f)
            rel = os.path.relpath(s, src)
            t = os.path.join(dst, rel)
            if not os.path.exists(t) or os.path.getmtime(t) < os.path.getmtime(s):
                yield rel


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sync a directory tree into another.")
    ap.add_argument("src")
    ap.add_argument("dst")
    a = ap.parse_args(argv)
    for rel in sorted(plan(a.src, a.dst)):
        os.makedirs(os.path.dirname(os.path.join(a.dst, rel)) or a.dst, exist_ok=True)
        shutil.copy2(os.path.join(a.src, rel), os.path.join(a.dst, rel))


if __name__ == "__main__":
    main()
