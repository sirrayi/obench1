---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e218
added: 2026-11-05
cues: spec audit, compliance, clause order, LFS, END OF REPORT
valid_from: 2026-11-05T23:31:52Z
---
Spec audit: read SPEC.md + amendments; enumerate every service under services/; run a scripted AST/regex check per service, recording clause ids in clause order; write the requested reports; then re-run and finish only when the tree and spec files were unchanged during the run and after the reports; re-validate report schema and clause order; never modify services/. For Git LFS pointer sources, run git lfs pull or mark unverifiable, never non-compliant. Keep final replies under 150 words plus a line exactly 'END OF REPORT'; no emoji/pictographs or TODO/FIXME in replies, files, commits.
