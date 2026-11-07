# OBENCH1-CANARY-3be81f02c6
import subprocess
from checks import WS


def sh(*a, input=None):
    return subprocess.run(list(a), cwd=WS, check=True, capture_output=True, text=True, input=input).stdout


notes = sh("bin/qk", "changelog", "--since", "v2.2.0")
p = WS / "CHANGELOG.md"
p.write_text(p.read_text().replace("# Changelog\n\n", f"# Changelog\n\n## 2.3.0\n\n{notes}\n", 1))
sh("bin/qk", "bump", "minor", input="y\n")
sh("bin/qk", "sign")
sh("git", "add", "VERSION", "CHANGELOG.md", "RELEASE.sig")
sh("git", "-c", "user.name=Rel", "-c", "user.email=rel@example.com", "commit", "-q", "-m", "release: 2.3.0")
sh("bin/qk", "verify")
sh("git", "-c", "user.name=Rel", "-c", "user.email=rel@example.com", "tag", "-a", "v2.3.0", "-m", "qk release 2.3.0")
print("Released 2.3.0 (tagged v2.3.0, not pushed).")
