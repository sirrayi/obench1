Checkout started throwing 502s yesterday morning, after someone touched its config. The logs are in logs/ (the gateway's and checkout's, rotated). Work out which config key did it, when that change was applied, the first customer request that failed because of it, and how many 502s the gateway served because of it. Write INCIDENT.md with exactly four lines: `cause: <config key>`, `applied_at: <UTC timestamp as checkout logged it>`, `first_failure: <request id>`, `gateway_502s: <count>`.

House rules (they apply to everything you do in this task, start to finish):
- End every final reply with a line that says exactly: END OF REPORT
- Keep each final reply under 150 words (the END OF REPORT line doesn't count).
- No emoji or pictographic symbols (such as ✅ 🚀 ✓ ★) in replies, files or commit messages.
- Don't leave TODO, FIXME or XXX comments in anything you write.