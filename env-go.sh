# Source before `obench.py run`: OpenCode Go (the owner's subscription), deepseek-v4.1-flash,
# 1M context, 384K output. Field-run arms (2026-11-05): overseer (v5), omp, dsh, hermes, pi.
# Each harness keeps its built-in Go provider; only the base URL moves to the cell gateway,
# which forwards to Go and sends every model call with the same model, thinking on, effort
# max and 384K output (obench.py MODEL_PARAMS). Throwaway harness dirs live in
# results/harness-config; the owner's ~/.pi, ~/.omp, ~/.hermes and ~/.dsh are never touched.
HERE=${0:A:h}

# Overseer v5 by default (sha256s in results/pins.txt); named builds for side-by-side
# runs: `--agents overseer@v3,overseer@v4,overseer@v5`
export OVERSEER_BIN=$HOME/.cache/harness-pins/overseer-v5-rc2
export OVERSEER_BIN_V5=$OVERSEER_BIN
export OVERSEER_BIN_V4=$HOME/.cache/harness-pins/overseer-v4
export OVERSEER_BIN_V3=$HOME/.cache/harness-pins/overseer-v3
export OVERSEER_PROVIDER=opencode OVERSEER_BASE_URL=https://opencode.ai/zen/go/v1
export OVERSEER_MODEL=deepseek-v4.1-flash
export PI_CODING_AGENT_DIR=$HERE/results/harness-config/pi-agent PI_PROVIDER=opencode-go PI_THINKING=max
export OMP_AGENT_DIR=$HERE/results/harness-config/omp-agent OMP_PROVIDER=opencode-go OMP_THINKING=max
export HERMES_PROVIDER=opencode-go
# Hermes's tool installs and cache, shared by every cell's fresh Hermes home
export HERMES_SHARED_DIR=$HOME/.cache/harness-shared/hermes
# Every arm's own reasoning knob at its top, all with thinking on; the gateway
# then sends every model call with the same settings (obench.py MODEL_PARAMS)
# --max-steps / --max-cost: v5 ships with 100 steps and $5; both lifted so the wall cap is the only limit for every arm (owner, 2026-11-05)
# --no-sandbox: macOS can't start v5's own bash sandbox inside the cell's jail (exit 71 on every call in
# the pilot); the jail is the sandbox for every arm, and no other arm sandboxes its shell (2026-11-05)
export OVERSEER_EXTRA_FLAGS="--effort max --max-steps 100000 --max-cost 1000 --no-sandbox" DSH_EFFORT=max HERMES_REASONING=max
# The key is read from the keychain only for a real run: `obench.py wiring` never needs it.
if [[ $1 == --with-key ]]; then
  export OPENCODE_API_KEY=$(security find-generic-password -s opencode -a overseer -w 2>/dev/null)
  [[ -n $OPENCODE_API_KEY ]] || echo "no keychain item opencode/overseer"
fi
