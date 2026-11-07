---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e126
added: 2026-11-06
valid_from: 2026-11-06T00:29:59Z
---
packages/web deliberately does not import from the edge package; when web needs behavior edge already has (e.g. clock or date helpers), add small local helpers in web instead of adding a cross-package dependency.
