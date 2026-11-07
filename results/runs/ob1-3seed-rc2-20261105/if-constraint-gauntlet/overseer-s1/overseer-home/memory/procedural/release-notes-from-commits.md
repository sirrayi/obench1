---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e230
added: 2026-11-05
cues: release notes, commits.jsonl, byte-for-byte, RELEASE_NOTES.md
valid_from: 2026-11-05T18:50:08Z
---
(1) Treat the request's rule list as authoritative; it supersedes docs/RELEASING.md and tools/notes.py, which document the prior release. (2) Build entries from commits.jsonl, applying filters in the given order (reverts/reverted commits, internal exclusions, dependency renames); normalize text before appending markers. (3) Map contributor emails via .mailmap. (4) Keep scratch scripts in /tmp so only the deliverable lands in the workdir. (5) Verify with an independent script re-deriving expected entries; compare content, order and byte-level formatting.
