#!/bin/zsh
# OBench1 3-seed run, 2026-11-05: 3 seeds, 27 tasks, arms overseer (v5), omp, dsh, pi, hermes, in lockstep
# (one task and seed at a time, the five arms side by side). Go subscription, deepseek-v4.1-flash, max effort.
# Started 13:4x UTC Thursday, inside Go's off-peak hours (10-01 UTC); about 10.5 h at the pilot's pace, so it
# should end around 00:15 UTC. Keeps the Mac awake and runs the watcher alongside. No spend stop (owner).
cd /Users/r23/Desktop/OBench1
source env-go.sh --with-key
caffeinate -is python3 obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 3 --run-set ob1-3seed-20261105 > results/watch/ob1-3seed-20261105/runner.log 2>&1 &
RP=$!
python3 lib/watch.py --run-set ob1-3seed-20261105 --runner-log results/watch/ob1-3seed-20261105/runner.log --runner-pid $RP --out results/watch/ob1-3seed-20261105 --every 30
wait $RP
echo "runner exit $?" >> results/watch/ob1-3seed-20261105/events.log
