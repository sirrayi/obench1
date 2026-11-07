---
provenance: review:session:p2
confidence: 0.6
source: overseer:session/p2#e158
added: 2026-11-05
cues: issue does not reproduce, stale bug report, already fixed, triage
valid_from: 2026-11-05T22:06:09Z
---
1) Run the issue's reproduction command on HEAD before changing anything. 2) If it does not reproduce, search history for the commit that fixed the root cause and run the full test suite on the unchanged tree. 3) Confirm the reported symptom by exporting the pre-fix commit into a temp worktree, running the same command there, and running the current tests against it to show they catch it. 4) Report already-fixed with matching figures for both, and make no code change.
