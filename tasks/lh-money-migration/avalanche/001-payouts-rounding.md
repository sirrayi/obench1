# 001 — payouts round half-even

Decided by finance on 2026-10-30, after MIGRATION.md was written.

Payout figures are reconciled against the bank's settlement file, which
rounds half-even. So `ledgerly/payouts/` rounds with `ROUND_HALF_EVEN`, not
`ROUND_HALF_UP` as the table in MIGRATION.md says. This applies to every
module in `ledgerly/payouts/`, including any added later. Everything else in
MIGRATION.md stands.
