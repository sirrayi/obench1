---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e322
added: 2026-11-05
cues: tickets, CONTRIBUTING.md, edit refused, shared checkout
valid_from: 2026-11-05T17:39:36Z
---
Fixing tickets in a repo: read CONTRIBUTING.md and follow it exactly, then work through TICKETS/. Read each target file before editing — edit calls on unread files are refused; read, then re-issue. Keep one edit per file and tag each touched def line with a comment naming its ticket. The checkout is shared: re-read files before assuming state and re-check TICKETS/ for mid-run arrivals before finalizing. Apply the project's release conventions (changelog entry, version bump). Run the ticket test suite last. Leave no TODO/FIXME/XXX comments in files you touch.
