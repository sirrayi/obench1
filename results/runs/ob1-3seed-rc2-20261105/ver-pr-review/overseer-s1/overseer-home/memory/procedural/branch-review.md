---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e154
added: 2026-11-06
cues: review, pull request, branch, worktree, findings
valid_from: 2026-11-06T03:11:25Z
---
Review a branch against main: 1) read the diff/commits for intent. 2) Run the branch's tests in a detached worktree (`git worktree add --detach <dir> <sha>`), leaving branch and main untouched. 3) Check tests assert the behavior; a green suite that never asserts a rejection proves nothing. 4) Reproduce each defect against a live server before reporting it. 5) Write REVIEW.md one finding per line as `<file>:<line>: <blocker|major|minor>: <what's wrong>`, with branch line numbers and only real defects, no style nits. 6) Remove the worktree; leave only REVIEW.md.
