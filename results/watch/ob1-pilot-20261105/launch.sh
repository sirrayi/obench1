#!/bin/zsh
# OBench1 pilot, 2026-11-05: 1 seed, 27 tasks, arms overseer (v5), omp, dsh, pi, hermes, in lockstep
# (one task at a time, the five arms side by side). Go subscription, deepseek-v4.1-flash, max effort.
# Waits for 04:01 UTC (end of Go's 01-04 UTC double-price window), keeps the Mac awake, and runs the
# watcher alongside. No spend stop (owner, 2026-11-05: "can go all in").
cd /Users/r23/Desktop/OBench1
while [[ $(date -u +%H%M) -lt 0401 ]]; do sleep 30; done
source env-go.sh --with-key
caffeinate -is python3 obench.py run --agents overseer,omp,dsh,pi,hermes --seeds 1 --run-set ob1-pilot-20261105 > results/watch/ob1-pilot-20261105/runner.log 2>&1 &
RP=$!
python3 lib/watch.py --run-set ob1-pilot-20261105 --runner-log results/watch/ob1-pilot-20261105/runner.log --runner-pid $RP --out results/watch/ob1-pilot-20261105 --every 30
wait $RP
echo "runner exit $?" >> results/watch/ob1-pilot-20261105/events.log
