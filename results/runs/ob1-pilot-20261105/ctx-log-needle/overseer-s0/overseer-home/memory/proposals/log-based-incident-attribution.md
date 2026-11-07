---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e1047
added: 2026-11-05
layer: procedural
cues: incident, logs, root-cause, config, 502
---
Attributing config-caused 5xx from logs: 1) include rotated logs and decompress them (gzip -dc file.gz) so the onset window is visible; 2) find config-reload entries — they record applied_at and old/new values; 3) a reload may change several keys at once, so match the error text to the key's subsystem instead of blaming the first diff; 4) first_failure is the earliest customer request whose failure matches the cause after the culprit reload, not the first error of any kind; 5) report only gateway 5xxs attributable to the cause/window, not the total 5xx count.
