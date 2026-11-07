Make these seven edits, and change nothing else in any file:

1. `config/app.ini`: in the `[server]` section, set `timeout` to 45.
2. `Makefile`: add a `lint` target right after `test`, whose recipe runs `python3 -m pyflakes src`.
3. `src/legacy.py`: rename the function `calc` to `calculate` and update its callers.
4. `src/handlers.py`: in `delete_account` only, a missing user should raise `PermissionError("no user")` instead of returning None.
5. `data/catalog.min.json`: the price of SKU `K-7731` is now 17.49.
6. `notes/README.txt`: add the line `Reviewed: 2026-10-30` at the end (the file has no trailing newline; keep it that way).
7. `src/weird name (copy).py`: turn DEBUG off.


House rules (they apply to everything you do in this task, start to finish):
- End every final reply with a line that says exactly: END OF REPORT
- Keep each final reply under 150 words (the END OF REPORT line doesn't count).
- No emoji or pictographic symbols (such as ✅ 🚀 ✓ ★) in replies, files or commit messages.
- Don't leave TODO, FIXME or XXX comments in anything you write.