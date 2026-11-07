---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e160
added: 2026-11-05
cues: config reload, 502, log triage, request id, revert
valid_from: 2026-11-05T18:06:26Z
---
Config-change 502 triage: find config reload lines with timestamp and old->new values. For each key, verify errors start only after its reload. Find the first actual failed request, then match its id across gateway and backend logs to attribute the error. Exclude pre-existing baseline errors before counting; confirm at the revert, where errors stop. Pitfall: an unreverted key in the same reload can still be innocent. Pitfall: gateway 502 totals include unrelated baseline failures—count only ids tied to the backend failure.
