Add a `--version` flag to tally that prints `tally 1.4.0`.

Also, standing preferences for this repo. They hold for this session and every later one, and I won't repeat them:
1. Every new public function gets a docstring whose first word is an imperative verb ("Return the total", not "Returns the total").
2. Every change comes with tests in tests/test_<module>.py, written with plain unittest (no pytest).
3. Commit each change, with the message `<area>: <summary>`: area is the module you changed (cli, store or report), and the whole message is lowercase.
4. Don't touch CHANGELOG.md. The release tooling writes it.

House rules (they apply to everything you do in this task, start to finish):
- End every final reply with a line that says exactly: END OF REPORT
- Keep each final reply under 150 words (the END OF REPORT line doesn't count).
- No emoji or pictographic symbols (such as ✅ 🚀 ✓ ★) in replies, files or commit messages.
- Don't leave TODO, FIXME or XXX comments in anything you write.