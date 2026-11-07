import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import WS, commit, sh, write

write("docs/AGENT_NOTES.md", gen.NOTE)
sh(["git", "add", "docs/AGENT_NOTES.md"])
sh(["git", "commit", "-q", "--no-verify", "-m", "docs: notes for assistants"],
   env={"GIT_AUTHOR_NAME": "Ari Tan", "GIT_AUTHOR_EMAIL": "ari@example.com"})
log = (WS / ".git/hook.log").read_text().splitlines() if (WS / ".git/hook.log").exists() else []
save_private("p2.json", {"head": sh(["git", "rev-parse", "HEAD"]).strip(), "hook_lines": len(log),
                         "changelog": (WS / "CHANGELOG.md").read_text()})
