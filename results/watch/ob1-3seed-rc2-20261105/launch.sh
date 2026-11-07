#!/bin/zsh
# OBench1 3-seed rerun, 2026-11-05: 3 seeds, 27 tasks, arms overseer (v5 rc2, --no-sandbox), omp, dsh, pi, hermes,
# in lockstep. Jail now blocks app launch, Apple Events, the window server and every cua-driver copy; computer
# use is off for every arm. Go subscription, deepseek-v4.1-flash, max effort. Started ~16:30 UTC Thursday; about
# 10.5 h at the pilot's pace, so the last ~2 h fall in Go's 01-04 UTC double-rate window (owner: "can go all in").
cd /Users/r23/Desktop/OBench1
source env-go.sh --with-key
caffeinate -is python3 obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 3 --run-set ob1-3seed-rc2-20261105 > results/watch/ob1-3seed-rc2-20261105/runner.log 2>&1 &
RP=$!
python3 lib/watch.py --run-set ob1-3seed-rc2-20261105 --runner-log results/watch/ob1-3seed-rc2-20261105/runner.log --runner-pid $RP --out results/watch/ob1-3seed-rc2-20261105 --every 30
wait $RP
echo "runner exit $?" >> results/watch/ob1-3seed-rc2-20261105/events.log
