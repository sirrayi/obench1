---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e3711
added: 2026-11-05
layer: semantic
cues: accounts, fetch_user, load_account, with_deleted
---
harbor accounts API: accounts.load_account(..., with_deleted=...) is the canonical user lookup; accounts.fetch_user remains only as a deprecated wrapper that warns then delegates and is deliberately excluded from __all__. New code and tests should call load_account and pass with_deleted instead of reaching for fetch_user.
