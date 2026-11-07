Write INVENTORY.md for everything under data/: one line per regular file (not directories, links or anything else), `<path relative to data/> | <size in bytes> | <first 12 hex of its sha256>`, sorted by path. If a file can't be read, put `unreadable` instead of the hash. Then a last line `invoice_lines: <n>`: how many lines across those files contain `invoice` (case-sensitive). Don't change anything under data/.

House rules (they apply to everything you do in this task, start to finish):
- End every final reply with a line that says exactly: END OF REPORT
- Keep each final reply under 150 words (the END OF REPORT line doesn't count).
- No emoji or pictographic symbols (such as ✅ 🚀 ✓ ★) in replies, files or commit messages.
- Don't leave TODO, FIXME or XXX comments in anything you write.