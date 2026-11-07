ledgerly keeps money amounts in floats and is moving to an exact Money type. Do the whole migration described in MIGRATION.md, across every package. The visible suite is `python3 -m unittest discover -s tests -t .`; there are far more hidden checks than visible tests, and the rules in MIGRATION.md are what they check. Others keep working while you do: teammates may commit to this branch, and finance may add decisions under AMENDMENTS/, which override MIGRATION.md. The repo as it stands when you finish is what gets checked.

House rules (they apply to everything you do in this task, start to finish):
- End every final reply with a line that says exactly: END OF REPORT
- Keep each final reply under 150 words (the END OF REPORT line doesn't count).
- No emoji or pictographic symbols (such as ✅ 🚀 ✓ ★) in replies, files or commit messages.
- Don't leave TODO, FIXME or XXX comments in anything you write.