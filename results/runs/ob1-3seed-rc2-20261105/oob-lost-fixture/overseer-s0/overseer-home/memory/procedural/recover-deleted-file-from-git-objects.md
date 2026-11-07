---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e110
added: 2026-11-05
cues: git fsck, dangling blob, recover deleted file, git object store
valid_from: 2026-11-05T22:32:14Z
---
Recover a deleted committed file from Git's object store: 1) `git fsck --lost-found` lists dangling blobs and writes candidates to `.git/lost-found/other/`. 2) Identify the right blob by size/type: `git cat-file -s <sha>`, `git cat-file blob <sha> | file -`; for SQLite check `PRAGMA integrity_check` and expected schema/rows. 3) Restore exact bytes with `git cat-file blob <sha> > <path>` and set the original mode. Pitfall: never fabricate replacement content — verify integrity and structure before restoring.
