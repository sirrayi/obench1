import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private, tree_digest, WS
from fixture import write

write("commits.jsonl", gen.jsonl(gen.commits()))
write(".mailmap", gen.MAILMAP_TEXT)
write("README.md", "# relkit\n\nRelease tooling for the platform monorepo. Release notes are written from\n"
      "`commits.jsonl`, an export of the commits since the last tag.\n")
write("CHANGELOG.md", "# Changelog\n\n## 4.1.0\n\n- See the 4.1.0 release notes.\n\n## 4.0.0\n\n- First release on the new platform.\n")
write("docs/RELEASING.md", """# Releasing (4.1)

1. Export the commits: `scripts/export-commits > commits.jsonl`.
2. Run `python3 tools/notes.py commits.jsonl > RELEASE_NOTES.md`.
3. Check the sections look like this:

```
# 4.1.0 release

### Breaking
* api: something (#12) [abc1234]

### Features
### Bug fixes
### Performance
### Thanks to
* Name
```
""")
write("tools/notes.py", '''"""Release notes from a commits.jsonl export (4.1 format)."""
import json
import sys

SECTIONS = [("breaking", "Breaking"), ("feat", "Features"), ("fix", "Bug fixes"),
            ("perf", "Performance")]


def main(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    rows.sort(key=lambda r: r["date"], reverse=True)
    out = {k: [] for k, _ in SECTIONS}
    people = set()
    for r in rows:
        head = r["message"].splitlines()[0]
        if ":" not in head:
            continue
        kind, summary = head.split(":", 1)
        scope = "general"
        if "(" in kind:
            kind, scope = kind.rstrip(")").split("(", 1)
        if kind.endswith("!") or "BREAKING CHANGE" in r["message"]:
            kind = "breaking"
        kind = kind.lower().rstrip("!")
        if kind in out:
            out[kind].append(f"* {scope}: {summary.strip()} [{r['hash'][:7]}]")
            people.add(r["author"])
    print("# 4.1.0 release\\n")
    for k, title in SECTIONS:
        print(f"### {title}")
        print("\\n".join(out[k]) + "\\n")
    print("### Thanks to")
    print("\\n".join(f"* {p}" for p in sorted(people)))


if __name__ == "__main__":
    main(sys.argv[1])
''')
save_private("digest.json", tree_digest(WS))
