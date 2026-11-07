---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e89
added: 2026-11-06
cues: rename, minimal diff, preserve formatting, line endings
valid_from: 2026-11-06T00:41:17Z
---
1) Before editing, read the target region and check file quirks: `file <path>` for encoding, `grep -n` for the symbol. 2) Make the smallest edit that satisfies the request; touch no adjacent lines. 3) For renames, match whole identifiers (`grep -nw old`) so lookalike names built from the old name stay untouched, and update every call site. 4) Verify the diff shows only intended lines, then run the relevant check (`make -n <target>`, `python3 -m pyflakes src`). Pitfall: whole-file rewrites silently flip CRLF→LF or latin-1→UTF-8, so write bytes back in the original encoding.
