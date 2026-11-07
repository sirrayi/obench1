---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e137
added: 2026-11-06
cues: i18n, gettext, translation, catalog, format string
valid_from: 2026-11-06T00:23:45Z
---
Translatable strings must be literal templates passed to `_()`, with interpolation applied after translation: `_('%d items skipped') % n`. Interpolating before the call (f-string, or % inside the literal) prevents message-catalog extraction.
