# OBENCH1-CANARY-3be81f02c6
from checks import WS

(WS / "VERDICT.md").write_text("""verdict: don't merge
issue_repro: fail
branch_tests: pass
test_checks_the_fix: no

The branch's tests pass, but the issue's own repro still fails: the export uses CRLF, and the fix only rejoins
LF-split lines, so the second row still loses its note. The new test only covers LF, and its second assertion
expects `x, y` to split into two fields, which is the old splitting bug written down as expected output.
""")
print("Don't merge: tests pass but the CRLF repro from #42 still fails, and the new test encodes buggy output.")
