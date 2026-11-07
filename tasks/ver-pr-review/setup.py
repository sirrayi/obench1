import os
import sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
from checks import save_private
from fixture import commit, git_init, sh, write

for p, t in gen.BASE.items():
    write(p, t)
git_init()
commit("server skeleton")
sh(["git", "checkout", "-q", "-b", "feature/rate-limit"])
where = {}
for p, t in (("app/limiter.py", gen.LIMITER), ("app/handlers.py", gen.HANDLERS), ("tests/test_limiter.py", gen.TEST)):
    write(p, gen.strip(t))
    for tag, n in gen.lines_of(t).items():
        where[tag] = [p, n]
write("docs/limits.md", gen.DOCS)
commit("Add per-client rate limiting", author=("Sam Okafor", "sam@example.com"))
sh(["git", "checkout", "-q", "main"])
lim = gen.strip(gen.LIMITER).splitlines()
where["leak"] = ["app/limiter.py", [i for i, l in enumerate(lim, 1) if "self.buckets = {}" in l][0],
                 [i for i, l in enumerate(lim, 1) if "self.buckets[key] = b" in l][0]]
refs = sh(["git", "for-each-ref", "--format=%(refname) %(objectname)"])
save_private("truth.json", {"where": where, "refs": refs})
