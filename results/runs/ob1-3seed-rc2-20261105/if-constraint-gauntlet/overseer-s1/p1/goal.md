Write RELEASE_NOTES.md for release 4.2.0 from commits.jsonl (one JSON object per line: hash, author, email, date, message). The result is compared byte for byte, so follow these rules exactly. docs/RELEASING.md and tools/notes.py describe the 4.1 process; these rules supersede both.

1. The first line is `# Release 4.2.0`, followed by a blank line.
2. Sections, in this order: `## Breaking changes`, `## Features`, `## Fixes`, `## Performance`, then `## Contributors`. Leave out any section that would have no entries. Each section heading is followed by a blank line, then its entries, then a blank line (except the last section, which ends the file with its last entry).
3. A commit's header is the first line of its message. Only headers that exactly match `<type>[(<scope>)][!]: <summary>` count: lowercase type, a scope with no spaces or parentheses, one space after the colon. Anything else (for example `Feat: x`, `fix:x`, `fix (api): x`) is ignored, and nothing in a message body is ever a header.
4. Only feat, fix and perf commits go in, with one exception: a header with `!` right before the colon is a breaking change, whatever its type, and goes only in Breaking changes. A `BREAKING CHANGE:` footer without the `!` does not make a commit breaking.
5. Non-breaking feat goes in Features, fix in Fixes, perf in Performance.
6. Leave out commits whose scope is `internal`, unless they are breaking.
7. Leave out every revert commit (header starting `Revert "`) and every commit a revert names in its `This reverts commit <hash>.` line.
8. Entry format: `- **<scope>:** <summary> (<hash7>)`, where hash7 is the first 7 characters of the hash. A commit with no scope uses `general`. In the summary, capitalise the first character and remove one trailing period if there is one; change nothing else.
9. For fix commits (breaking ones too), each body line that is exactly `Fixes #<n>` adds ` (#<n>)` after the summary and before the hash, in the order the lines appear. Other phrasings (Clos