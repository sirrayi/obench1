---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e182
added: 2026-11-05
cues: incident, 502, config, logs, triage, checkout
valid_from: 2026-11-05T17:54:10Z
---
When a service behind a gateway starts failing after a config change: 1) Search rotated service and gateway logs for config reload entries and diff changed keys (old -> new). 2) Isolate the key whose change precedes symptom onset; don't blame sibling changed keys without evidence. 3) Find the first failing request id in the service log. 4) Correlate gateway 502s to service 500s by request id after normalizing timestamps. 5) Count only failures attributable to the change; exclude pre-existing failure classes such as upstream timeouts.
