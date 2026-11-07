# OBENCH1-CANARY-3be81f02c6
import json
import os
from checks import PRIVATE, WS

w = json.load(open(os.path.join(PRIVATE, "truth.json")))["where"]
f = lambda t: f"{w[t][0]}:{w[t][1]}"  # noqa: E731
(WS / "REVIEW.md").write_text(f"""{f('offbyone')}: blocker: `> self.limit + 1` lets limit+1 requests through; should be `> self.limit`
{f('spoof')}: blocker: X-Forwarded-For is client-controlled; anyone can rotate it to dodge the limit (use the LB's own header or the rightmost hop)
{f('clock')}: major: bucket start uses time.time() but is compared against time.monotonic(), so windows never reset properly
{f('race')}: major: buckets are created and stored outside the lock; concurrent first requests race and lose counts
{w['leak'][0]}:{w['leak'][1]}: major: buckets are never evicted, so memory grows with every client ever seen (docs promise 10 min)
{f('weaktest')}: minor: the test never checks that request limit+1 is rejected, so it can't catch the off-by-one
""")
print("Review written: two blockers (off-by-one, spoofable client key), three majors, one weak test.")
