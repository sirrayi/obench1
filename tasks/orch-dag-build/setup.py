import json
import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from fixture import commit, git_init, write

write("specs/RULES.md", gen.RULES_MD)
for svc in gen.SVCS:
    write(f"specs/{svc}.md", gen.spec(svc))
    ex = [r for r in gen.records(svc, 40, "examples") if all(not k.startswith("inv_code") for k in r)] if svc in ("invoices", "payments") \
        else gen.records(svc, 40, "examples")
    ex = [{"record": r, "result": gen.outcome(lambda x: gen.normalize(svc, x), r)} for r in ex[:3]]
    write(f"examples/{svc}.json", json.dumps(ex, indent=1, ensure_ascii=False) + "\n")
write("clients/__init__.py", "")
write("README.md", "# normalizers\n\nOne normalizer per service; see specs/. Results are compared exactly (types included).\n")
git_init()
commit("normalizer specs")
