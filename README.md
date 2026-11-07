# OBench1

OBench1 is a benchmark for coding-agent harnesses. Every harness gets the same model, the same settings and the same tasks at the same moment, so what's being measured is the harness: how it manages context, handles tools that misbehave, keeps to the rules, remembers across sessions and reports honestly on what it did.

This repository is the whole thing: the runner, the harness adapters, all 27 tasks with their graders and reference solutions, and every result from the first full run, transcripts included. The write-up of that run is at [ovrhq.dev/docs/obench1](https://ovrhq.dev/docs/obench1/).

## What's here

| Path | What it is |
|---|---|
| `obench.py` | The runner and CLI: cells, phases, avalanches, the jail, the report |
| `panel.py` | The 15 category judges and the house rules |
| `harnesses/` | One adapter per harness (Overseer, omp, dsh, pi, Hermes, a bare loop, and `generic` for any CLI harness), plus the jail |
| `lib/` | Shared by the runner and the graders: the metering gateway, the fault proxy, the fake upstream, checks and fixtures |
| `tasks/<id>/` | `task.json`, `setup.py`, `grade.py`, `oracle.py`, and `gen.py`, `between.py` or `avalanche/` where a task needs them |
| `env-go.sh` | The environment for the first run: model, provider, pinned builds, each harness's reasoning setting |
| `DESIGN.md` | The design as written before the first run, rules and all |
| `results/` | Everything the first run produced (below) |
| `backups/` | Two files as they were before last-minute fixes on 5 November |

## The tasks

27 tasks across 15 categories, from a one-line job that measures fixed overhead to a rename across about 1,200 files that runs past 2M tokens. Each one has a reference solution that passes its grader, and a do-nothing agent scores zero on every one. `DESIGN.md` has the full table, and each task's `task.json` holds its instruction, limits and metric checks.

Some tasks hit every harness with the same disruption partway through its run: a spec amendment, a teammate's commit, a log flood, or a storm of provider faults.

## Running it

You need macOS (the jail is built on `sandbox-exec`), the system `python3`, and the harnesses you want to compare. Every model call goes through a gateway on loopback that meters it and sets the same model parameters for everyone.

```bash
python3 obench.py list
python3 obench.py oracle-check     # reference solutions must pass
python3 obench.py null-check       # a do-nothing agent must score 0
python3 obench.py wiring --agents overseer,omp,dsh   # free: proves every harness goes through the gateway
source env-go.sh --with-key && python3 obench.py run --agents overseer,omp,dsh --seeds 3   # paid
python3 obench.py report --run-set <id> --by-category
```

`env-go.sh` reads the provider key from the macOS keychain and points at builds pinned under `~/.cache/harness-pins` (their sha256s are in `results/pins.txt`). Change it to fit your machine. To add a harness without writing an adapter, use `generic@<label>` with `OBENCH_GENERIC_CMD` (see `DESIGN.md`, "Running it").

A full run of 405 cells took 10 h 52 min on one Mac and cost $5.78 on the OpenCode Go plan with deepseek-v4.1-flash.

## Results

`results/` is left as the run produced it:

- `internal.jsonl`: one line per cell, with its build, timings, tokens and cost.
- `sealed/verdicts.jsonl`: every check, score and judge vote. During the run these were kept from anyone working on Overseer. They're open now.
- `runs/<run set>/<task>/<harness>-s<seed>/`: each cell's sessions, replies, diffs, the harness's own home directory and its metrics. `ob1-3seed-rc2-20261105` is the run the docs report. `ob1-pilot-20261105` and `ob1-3seed-20261105` are the void pilot and the run that was stopped. The `dryrun-*` and `wiring` sets are checks made before the paid runs.
- `reports/`: the final report and its build scripts, the pilot report and the first docs draft.
- `notes/`: the working notes kept during the run, including every problem found and how it was handled.
- `watch/`: the launch scripts and the live watch logs.

## Before you read the transcripts

- **One key was redacted.** In three cells pi ran `env`, which printed the provider key the run used. The key was revoked on 6 November. Its 42 appearances in pi's transcripts, and in the masked form Hermes logs, now read `oc_sk_REDACTED`. Nothing else was changed.
- **The other secrets are fake.** The deploy and archive tokens, Stripe keys and the like are planted by the tasks. The `ghp_xxxx`, `pat_your…here` and `you@gmail.com` strings come from documentation that ships with Hermes.
- **Paths name the machine.** Transcripts show the run's home directory, its temp folders and its shell prompt.
- **Nested repositories are renamed.** Many cells hold git repositories of their own: Overseer's memory folders, and workspaces the harnesses committed to. Git can't store a `.git` folder inside another repository, so each one is saved as `.git.saved` with every file intact. To bring them back after cloning, run `find results -depth -name .git.saved -type d -execdir mv .git.saved .git \;`. Files that the cells' own `.gitignore`s would hide are included too. Symlinks are kept as links, so the ones that pointed at a harness's shared cache or the app bundle on the run's machine now point nowhere. The gateways' Unix sockets aren't stored.
- **Harness files keep their own licences.** Each cell holds files its harness wrote or shipped, such as Hermes's bundled skills and pi's and omp's session logs. They're here as a record of the run and stay under their authors' licences.

## Who made it

The Overseer team wrote OBench1, and also builds Overseer, one of the harnesses it compares. The docs' [limits page](https://ovrhq.dev/docs/obench1/limits) explains what that means for the result.

## Licence

Licensed under either of [Apache License, Version 2.0](LICENSE-APACHE) or [MIT](LICENSE-MIT), at your option, except for third-party files under `results/` as noted above.
