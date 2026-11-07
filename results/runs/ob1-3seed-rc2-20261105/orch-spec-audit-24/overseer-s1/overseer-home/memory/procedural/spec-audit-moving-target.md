---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e255
added: 2026-11-05
cues: spec-audit, amendments, re-run, findings, scratch-files
valid_from: 2026-11-05T23:46:53Z
---
Auditing services against a spec: read SPEC.md and every SPEC-AMENDMENT-*.md (amendments add clauses). Script the audit, run it over all services under services/, and write the findings; never modify services/. Because the spec can be amended and teammates can land fixes mid-task, re-read the spec and re-run the audit before finishing; verify every findings file matches current HEAD and regenerate any mismatch. Write audit scripts to a fresh unique path; never overwrite an existing scratch file from another checkout.
