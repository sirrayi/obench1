---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e202
added: 2026-11-05
cues: incident, config change, root cause, 502, log triage
valid_from: 2026-11-05T18:19:52Z
---
Config-change incident triage: 1) Search all rotated logs of the affected service for reload entries; record each changed key and its logged UTC timestamp. 2) Test each key against the failure signature, not just timing—unrelated keys can change in the same reload. 3) Find the first request that failed for the suspect reason, not the first warning. 4) Correlate gateway errors with backend 5xx by request id/time; count only errors attributable to the cause. 5) Exclude error classes present before the change and after revert as pre-existing.
