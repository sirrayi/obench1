---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e95
added: 2026-11-06
cues: delete_account, PermissionError, src/handlers.py
valid_from: 2026-11-06T00:36:55Z
---
src/handlers.py deliberately keeps two missing-user styles: delete_account raises PermissionError("no user"), while the other handlers return None. Preserve that split; don't normalize one style to the other.
