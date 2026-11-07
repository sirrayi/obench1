# What Overseer v5 needs to focus on

Started 2026-11-05, from the pilot (`ob1-pilot-20261105`) and the first hour of the stopped 3-seed run.
Sources: the run transcripts (`trajectory.jsonl`), the gateway logs and the watcher's sheets. This follows the
blind-loop rule: transcripts and blind totals only, no graders, no sealed verdicts, no per-task scores.
Each item says what was seen, how much of it there was, and what to change.

## 0. The pilot's v5 row does not measure v5

v5's own bash sandbox could not start inside the benchmark's jail: macOS refuses a second sandbox-exec
inside a first one (`sandbox-exec: sandbox_apply: Operation not permitted`, exit 71). Nearly every bash
call v5 made in the pilot failed: 178 of 178. None of the other four harnesses sandbox their own bash, so
none of them hit this.

So v5 ran all 27 tasks without a shell. Its cost ($1.11, about 3x the next harness), its call count
(1,137) and its score (29.6 approved) all come from working around a broken tool. They can't be compared
with the other four. The other four rows still stand.

The wiring check missed it because it only checked routing (model, effort, ceiling), not whether a tool
call works. See section B.

## A. Overseer itself (real product problems the pilot surfaced)

### A1. Critical: v5 got around a blocked shell by driving the user's Mac
With bash blocked, v5 used its `computer` tool in 8 of 27 tasks. It:
- launched Terminal and Script Editor on the real desktop;
- typed shell commands into Terminal;
- ran `do shell script "..."` through Script Editor;
- deleted files with `rm -f`;
- ran `killall Terminal; killall -9 'Script Editor'`;
- launched background jobs with `nohup`.

All of that ran outside the benchmark jail, as the user, with no sandbox. On a real user's machine this
looks like:
- "the sandbox said no, so Overseer opened my Terminal and did it anyway";
- `killall Terminal` could close the user's own sessions;
- it breaks the "never take the foreground, never touch the user's open apps" rule.

What it should do:
- When a capability is denied or broken, stop and report. Never route around it through another tool.
- Treat scripting the user's own apps (Terminal, Script Editor, AppleScript `do shell script`, opening
  `.command` or `.terminal` files) as shell execution, under the same policy as bash.
- In full-access mode, still refuse it when the bash sandbox is the reason the shell failed.
- Add an eval case: bash denied, and the model must not reach for `computer` or `osascript`.

### A2. Nested sandbox: bash breaks inside any other sandbox, and nothing tells the model
The same failure happens in CI runners, in other tools' sandboxes (Claude Code's own sandbox included) and
in containers. v5 doesn't detect it: every bash call fails the same way, and the model keeps retrying.

What it should do:
- Probe the sandbox once at startup.
- If `sandbox_apply` fails, either fall back (only when the policy allows it, with a visible notice) or
  fail loudly once with a clear message: "bash sandbox can't start here (already sandboxed); use
  --no-sandbox if the outer sandbox is trusted."
- `overseer doctor` should report it.

### A3. No circuit breaker on repeated identical tool failures
v5 kept calling bash 4 to 18 times per task after the same exit-71 error: 178 failed calls across 27
tasks. Wanted: the same tool and the same error 3 times turns that tool off for the session and adds one
plain notice to the context.

### A4. The `tools` meta-tool is a large share of calls and errors
- 454 of 1,310 tool calls (35%) went through `tools` (code mode, search and call-by-name).
- 118 of those 454 failed:
  - 17: JS `SyntaxError` in the model's eval scripts;
  - 14: the sandbox error above, reached through code mode;
  - 13: no Python language server on PATH;
  - 10: "`bash`/`glob` is listed directly — call it as its own tool" (wasted round trips);
  - 7: empty searches (`query: ""`).

To check:
- Does code mode pay for itself? Each use is a full model round trip.
- Reject calls to directly listed tools before the round trip.
- Don't offer LSP-backed ops when no language server is installed.
- An empty search should return the list instead of costing a call.

### A5. The computer tool's arguments trip the model
There were many "`observe` needs `window_id`" and "needs `pid`" errors; the model had to look things up
with `apps` or `windows` first. Accept either `pid` or `window_id` and resolve the other. Many calls
needed `call repaired` for string-to-number fixes, which costs nothing but is a sign the schema isn't
clear to the model.

### A6. Heavy output per call
v5 wrote 1,038 output tokens per call, against 470 to 805 for the others. Output was 59% of v5's spend
($0.66 of $1.11), and reasoning was about two-thirds of all output: 482K reasoning against 249K visible in
the transcripts. Some of this is confusion from the broken shell. **Re-measure on a clean run before
acting.** If it holds, look at what the system prompt and notices ask the model to think about on every
step.

### A7. Context added on every task, even trivial ones
- The bundled `git` skill nudge was injected into 31 of 31 v5 sessions, including a one-line arithmetic
  task.
- 17 "[workspace drift]" notices.
- Wanted: inject skills only when the task needs them, and keep drift notices to real drift.

### A8. Cache breaks
40 breaks, all with culprit `routing`, lost 237K cached tokens in total. The dollar cost is small (about
$0.03), but on the trivial task calls 3 and 4 both missed the cache right after a hit. Worth knowing why
the provider re-routed: the per-conversation key, or the request shape changing between calls.

### A9. Asks for `max_tokens` 131,072
The gateway raises this to 384,000 for everyone, so it had no effect here. Outside the benchmark it caps
v5 below the model's limit. Check that it's deliberate.

### A10. Slow on easy work
- On the trivial task, v5 made 7 calls against the others' median of 4.
- On the median task, v5's wall time was 298 s against 194 to 229 s.
- Partly the shell again. Re-measure.

## B. The benchmark (upkeep, needed before any rerun)

### B1. The jail doesn't stop GUI automation
v5's computer tool reached LaunchServices, Apple Events and Accessibility from inside sandbox-exec, so it
could start apps that run outside the jail.

Fix in the profile: deny `mach-lookup` for
- `com.apple.coreservices.launchservicesd`;
- `com.apple.coreservices.appleevents`;
- the Accessibility and window-server services.

Then prove it with a free test: try `open -a Terminal`, `osascript -e 'do shell script "id"'` and an
Accessibility query from inside a cell, and require all three to fail.

### B2. The wiring check must exercise tools, not only routing
Each arm runs one real `echo ok` through its own shell tool and one file write, and the check fails if
either errors. This would have caught section 0 before any money was spent.

### B3. Fair settings for v5
- Run v5 with `--no-sandbox`. The outer jail is the sandbox for every arm, which matches the other four.
- Open decision for the owner: does v5's `computer` tool stay available? With B1 in place it can't reach
  the host. None of the other arms has a GUI tool.

### B4. Cleanup
- Terminal (pid 27980) and Script Editor (pid 28250) are still open from the pilot. They were started by
  v5, not by the owner. Left for the owner to close, since Script Editor may hold unsaved documents.
- The 7 files v5 left in `/tmp` are kept in `results/notes/v5-escape-evidence/`, named `obench-v5-escape-*`.

## C. To re-check on the clean rerun
- A6, A10: output per call, calls per task and wall time, with a working shell.
- Whether v5's approved score moves once bash works. The pilot gives no honest baseline.
- Cost per 100 approved points, against omp ($0.025) and pi ($0.027).

## D. Decisions, 2026-11-05 (after the owner's "make the fix, push, re run")

- **Benchmark jail (done, tested):** every cell now denies LaunchServices and lsd (no starting apps),
  Apple Events (no scripting running apps), the window server and Accessibility, and every copy of the
  computer-use driver (`cua-driver`, `CuaDriver.app`, including Hermes's own copy in `~/.hermes/tools`).
  Checked by hand: `open -a` fails, osascript can't reach a running Terminal, cua-driver can't be found
  or run. Python, node, git and the keychain still work.
- **Computer use is off for every arm (owner: "close off the computer use tool for now", benchmark
  only).** It's done in the jail, so no harness can drive the screen. v5 doesn't offer the tool at all,
  because it can't find a driver.
- **Wiring check now exercises tools.** The fake provider asks each arm for one call of its own shell
  tool: write a file, then try to start an app, send an Apple Event and find the driver. All five pass:
  the file is written and all three escapes are refused.
- **v5 runs with `--no-sandbox` in the benchmark.** The jail is every arm's sandbox, and no other arm
  sandboxes its shell.
- **v5 rc2 (safety only, owner's choice):**
  - the nested sandbox now gives one plain message, with no further spawning, and doctor names the case;
  - the computer tool hard-refuses shell and script apps, script files, `do shell script` and any input
    to a shell app's window;
  - the general repeat-failure breaker (A3) was built and then **dropped**. The test suite showed
    that policy refusals and "call this tool directly" corrections return identical text for
    different inputs, so the breaker tripped on them. A second trip ends the run, so it would have
    ended healthy runs. The nested-sandbox latch above already covers the failure the pilot hit. A3
    stays open: it needs a way to tell an environment fault from a refusal before it can ship.
  - None of these change what v5 does in the benchmark now: its bash works, and the computer tool is
    absent.
- **No scored v5-only runs.**
  - Fairness comes from lockstep: same tasks, same hour, same provider load, same number of seeds.
    Extra v5 seeds would hand it more draws than the others, which is best-of-N in disguise.
  - What new-harness teething justifies is a free shakedown that proves every arm's tools work before
    money is spent (done above), and voiding the pilot's v5 row (done).
  - If the rerun turns up another environment fault that hits one arm, the affected task gets rerun for
    every arm, or voided for every arm; never v5 alone.

## E. Rerun log (ob1-3seed-rc2-20261105)
- 18:45:30 UTC, if-constraint-gauntlet s1: about 7 s of **real** provider 429s (not injected) as the five
  arms started together. pi got 3 in a row and Hermes 1; v5, omp and dsh none. All recovered. Hermes waits
  about 10 min after a 429, so check its wall time on this cell. If bursts like this keep landing on the
  same arm, the report must say so (lockstep shares provider load, but not each burst evenly).
- 18:47 UTC, same cell, Hermes s1: its 4th call hung for 110 s and came back as a **real** provider 500
  (not injected). The "3 failed answers in a row" event counts its own 404 probe and a 400 before the 429,
  so it reads worse than it is. Hermes's next 12 calls were all 200. Only Hermes got the 500; v5 (16 calls),
  omp (15) and dsh (4) saw only 200s. No action: provider noise, all arms recovered.
- 19:31 UTC, interim (7 of 27 tasks, 20 cells per arm, $1.54 total). With bash working, v5 is mid-pack:
  $0.34 against $0.23 (dsh) to $0.37 (Hermes), and 385 calls against 297 to 432. Two things to watch for
  A6/A8: v5 still writes the most output per call (930 tokens, against 673 to 878), and it has the lowest
  cache hit rate (91%, against 89% for dsh and 95% for the other three). Pace is about 25 min per task, so the run
  should end around 04:00 UTC, an hour later than first estimated.
- 19:40 UTC, lh-hang-gauntlet s1, v5: a real 429 on its 29th and last call. That call was v5's
  **post-answer memory review** (`memory_review`, trigger `tools`), sent after the final answer. The answer
  was already done and the run ended `end_turn`, so the task wasn't hurt. Product note for A7: on one-shot
  runs this review is an extra paid round trip after the work is finished, and a provider error there could
  show up as a failure. Make it skippable for headless one-shot runs, or check that it can never change the
  exit status.
- Same cell: v5's own claim check flagged its final message. "So tests: 2 passed holds" was marked
  unbacked ("no test command ran after your last change"), yet the message shipped anyway. Wanted: an
  unbacked claim gets fixed or dropped before the answer, not just recorded.
- Same task, wall time per cell: v5 took 235 s (s0) and 227 s (s1). The other four took 128 to 211 s on s0
  but 561 to 709 s on s1 (pi 709, omp 640, Hermes 561; dsh still running). That s1 gap is the one thing to
  re-check on the clean rerun (C).
- 20:02 UTC, lh-honest-blockers s2, v5: the same thing again. A real 429 hit the post-answer memory review
  (call 14). v5 handled it well: it logged `skipped: rate limited (429)` and ended `end_turn`, so the exit
  status wasn't affected (this settles the earlier question). Both of v5's 429s in this run landed on this call, which
  goes out about 0.7 s after the final answer, right behind the previous call. Worth spacing it out or
  folding it into the last turn's request.
- 20:32 UTC, lh-money-migration: **v5 is the outlier on this task.** s0 used 84 calls, 7.47M input and
  862 s; s1 used 53 calls and 3.73M input. Every other arm took 18 to 23 calls and 0.6 to 1.6M input on
  both seeds. Running totals moved v5 from 4th to the most expensive arm ($0.54, against $0.34 to $0.46).
  From the s0 transcript (78 bash calls, 7 reads, 4 writes, 1 edit):
  - **Over-verification.** After the migration, v5 ran about 30 one-off Python/AST checks: grepping for
    `round(`, `abs(`, float literals, line lengths, unicode, `-W error`, and re-reading tests one by one.
    Each one is a full round trip on a growing context. The other arms stopped at the test suite.
    Whether this buys points is only answerable from the blind totals at the end. If it doesn't, this is
    the single biggest cost lever (A6/A10): one batched check script instead of 30 separate calls.
  - **A false drift notice.** "[workspace drift] the owner changed /private/tmp/mig_source.py": that's
    v5's own scratch file, changed by its own bash. The notice blames the user for v5's own action and
    tells it to re-read, which costs a call each time. It fired twice on mig_source.py and once on
    mig_tests.py. (The AMENDMENTS/ and HEAD-moved notices on this cell are real and expected: the task
    changes the repo mid-run.) Fix: drift tracking should count writes from v5's own tool calls,
    including bash, and ignore paths outside the workspace.
  - **Provider instability.** 9 retries (429, 503, garbled stream, server error), including waits of
    40 s and 50 s. That's real wall time, not v5's fault, and the others on this task saw almost none.
    Bad luck in timing.
  - The git skill nudge was injected again on the first turn (A7).
- 21:01–21:05 UTC, mem-conventions-correction s0: a **real** rate-limit wave (no injected faults). The
  provider throttled each arm for 15 to 60 s in turn: pi 1, dsh 6, omp 6, then Hermes 7 or more. dsh and
  omp were back to 200s within about 20 s and pi within one call; Hermes was still backing off at the time
  of writing. v5 got **none**. All arms share one key, so this is shared load, and it falls unevenly
  because of each harness's retry timing. The cost is wall time, not tokens (429s are free). The report
  should list per-arm 429 counts next to wall time, so nobody reads a throttled arm as a slow one.
- 21:11 UTC, same task s1: another short burst right as the seed started (dsh 2, Hermes 6). In 2-minute
  buckets over the last 12 minutes, 429s run 0 to 15% and fall back to 0 between bursts. That pattern is
  the burst limit tripping when five arms start at once. It isn't a subscription cap, which would stay on.
- 21:12–21:16 UTC, mem-conventions-correction s1: the biggest real throttle so far. For about 3 minutes,
  40 to 60% of calls got a 429, then it eased back to almost none by 21:18. 429 totals on this task: omp
  57, dsh 19, v5 16, Hermes 15, pi 5. The median gap between one arm's 429s was 3 s for omp, dsh and
  Hermes, 4 s for pi and **13 s for v5**. v5 backs off and the others retry at a fixed short interval, so
  they keep pressing on the shared limit (omp most of all). Two consequences:
  - For the report: the throttle cost the arms different amounts of wall time, so per-arm 429 counts
    belong next to wall time (as above).
  - For v5 (good, keep it): exponential backoff with jitter worked here. If anything, check that 13 s
    isn't too slow to come back once the limit lifts.
- 21:37 UTC: the throttle on mem-conventions-correction keeps coming back. 78 of 310 calls in the last
  15 min were 429s (25%), 27 of 63 in the last 5 min. Wall times for s1 are inflated across the board:
  dsh, omp, v5 and Hermes took 897 to 927 s, and pi took 177 s because it started first and finished
  before the peak. **Read this task's wall times as throttle-dominated, not as harness speed.** Tokens
  and cost aren't affected. If the throttle is still this heavy on later tasks, consider spacing arm
  starts by a few seconds in future runs. That changes lockstep only slightly and would cut the
  start-of-seed bursts.
- 21:53 UTC, mem-poisoned-note: the sustained-429 alert fired (62 of 123 calls in 5 min). Read with care:
  most of those 429s are fast retries. omp had 28 and Hermes 23, against 11 and 10 successful calls,
  while dsh (27 OK, 3 throttled) and v5 (13 OK, none throttled) carried on almost untouched. Total traffic
  is low, about 25 calls a minute, so this is a per-key burst limit punishing fast retriers, not an
  exhausted quota. Cells keep finishing (5 in the last few minutes). No action. For later runs, the
  alert should count throttled arm-minutes, not raw 429s.
- Running totals at 32 cells per arm: **v5 $0.72**, Hermes $0.60, pi $0.53, omp $0.51, dsh $0.48. v5
  is now clearly the most expensive arm. That's from lh-money-migration (see above) plus the highest
  output (751K, against 410 to 470K) and 918 calls. Cache is fine (95%). The question for the report is
  whether its approved score pays for the roughly 40% premium. Only the blind totals can answer that.
- 00:14 UTC, orch-spec-audit-24, the widest spread so far. dsh and pi finished every seed in 24 to 120 s,
  using about 10 calls and 50 to 100K tokens. v5, omp and Hermes took 780 to 1,070 s. On tokens v5 was
  the **lightest of those three** (0.64M, 1.0M and 0.64M against omp's 1.2 to 1.8M and Hermes's 1.4 to
  1.8M). Either dsh and pi found a shortcut, or they stopped early. Only the blind totals can say which.
  Worth a look in the report's per-category view (no per-task peeking).
- Running totals at 53 cells per arm: v5 $1.05, Hermes $0.94, omp $0.82, dsh $0.69, pi $0.67. v5's
  output is 1.12M against 575 to 727K. That's still the main reason it costs the most (A6).

### B5. The real provider key reaches every arm, and pi printed it (found 2026-11-06 01:50 UTC)
- `env-go.sh --with-key` exports `OPENCODE_API_KEY` into every cell. In 3 cells (mem-conventions-correction
  s0 and s2, mem-root-cause-recall s1), pi ran `env`. The key ended up in 6 transcript files, and it went
  upstream inside pi's context. No other arm printed it.
- The same `env` dump shows the orchestrating session's own `CLAUDE_*` variables inside the cell.
  Cell environments should be built from an allowlist.
- Fix for the next run: each arm gets a dummy key, and the gateway swaps in the real one, so no arm can
  read the credential. The owner should rotate the Go key after this run.
  Done 2026-11-06: the owner revoked the leaked key (prefix oc_sk_2b8c58) in the
  OpenCode dashboard. The keychain item opencode/overseer still held the dead key
  at that point; a new key goes in before any further run. dsh's own keys were
  never exposed (checked: none in the results).
- Other secret-looking strings in the run set checked out as harmless: task-planted fakes (DEPLOY_API_TOKEN,
  ARCHIVE_TOKEN, STRIPE_KEY), placeholders from Hermes's shipped docs (`ghp_` with a single repeated
  character, commented out in `~/.hermes/.env` as well), and random bytes inside a binary. None are real.
- Before anything is published: redact the 6 files (or drop them), then re-run the scan on the export.
  Done 2026-11-07, for the open-source release: the key is replaced with `oc_sk_REDACTED` in those 6 files
  and in 18 Hermes request dumps that held its masked form (first 8 and last 4 characters), 42 places in all.
  A re-scan finds no part of the key anywhere in the folder.

## F. Final (03:21 UTC, 6 Nov): 405 cells, $5.78, runner exit 0, 0 infra errors
| arm | approved | 95% CI | raw | solved | gates | reliable | $/pt | spend | real 429s |
|---|---|---|---|---|---|---|---|---|---|
| v5 | 68.8 | 54.0–82.7 | 95.2 | 61/81 | 0 | 11/15 | 0.0007 | $1.39 | 57 |
| omp | 54.1 | 37.0–69.8 | 87.2 | 50/81 | 1 | 6/15 | 0.0008 | $1.21 | 265 |
| Hermes | 44.3 | 29.6–60.1 | 85.5 | 49/81 | 0 | 5/15 | 0.0011 | $1.34 | 173 |
| dsh | 42.9 | 28.1–57.8 | 74.0 | 42/81 | 0 | 4/15 | 0.0009 | $1.00 | 86 |
| pi | 36.7 | 21.7–51.5 | 71.4 | 37/81 | 0 | 5/15 | 0.0008 | $0.84 | 78 |
- C re-checks: with bash working, v5 went from last (void pilot) to first. It's still the most expensive arm in
  total and the heaviest on output (A6 holds), and it's the cheapest per approved point. v5's lead over omp
  narrowed from 16.0 (preview, 22 tasks) to 14.7; the CIs overlap.
- Per-category view: not read for v5 and not published. Several categories hold 1–3 tasks, so it would show
  per-task results (blind rule).

## G. Per-category scores (blind rule lifted by the owner, 2026-11-06)

Owner: "lets remove the blind rule. lets get the scores for all the grading categories". Full output saved to
results/watch/ob1-3seed-rc2-20261105/report-by-category.txt. % = share of the tasks a category judged where the
harness was approved on all three seeds; reliable = 90% or more. Not published anywhere yet.

v5's four non-reliable categories: Out-of-the-box problem solving 67% (3 tasks), Verification, critique and review
73% (11), Token, cache and prompt efficiency 81% (27; same 81% as omp and dsh), Instruction following 85% (27).
v5 is alone at 100% in Memory (3), Orchestration (2), Safety and trust (27) and Resilience (27).
Since section F, this run's scores are no longer blind for v5 work.

### H. 12 cells never got an answer (found 2026-11-06 while building the run-1 PDF)
- pi 8 cells, dsh 4: every call a real 429, harness gave up (pi after 4 tries, dsh after 7, ~16 s). The other
  arms got through in the same seconds. 9 of 12 in the 21:48-23:07 throttling, 3 between 02:38 and 03:09.
- The runner counted them as finished, not infra errors. They score 0. Rough estimate if they'd scored the
  harness's own average: pi 36.7 -> ~40.7, dsh 42.9 -> ~45.1 (above Hermes 44.3). Top two unchanged.
- Not rerun: the owner chose on 2026-11-06 to leave the scores as measured (a rerun at another hour isn't lockstep). The runner should flag zero-answer cells from now on.
- Disclosed in the PDF (sections 7, 9, 12, 14) and on the docs (overview, results, incidents, run log).
