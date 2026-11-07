---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e196
added: 2026-11-06
cues: audit, spec, services, report
valid_from: 2026-11-06T00:05:08Z
---
Steps: read SPEC.md and note its revision; list every service under services/; scan for Git LFS pointer files first (a pointer makes a service unverifiable, not failing); check each clause with the strictest match available - AST for docstrings, print calls and secret literals, exact line and digest match for Dockerfiles, READMEs, CODEOWNERS, requirements; keep the audited tree read-only; re-read the spec and re-check the tree before writing reports, stating the revision and commit they cover; validate every report file before finishing.
