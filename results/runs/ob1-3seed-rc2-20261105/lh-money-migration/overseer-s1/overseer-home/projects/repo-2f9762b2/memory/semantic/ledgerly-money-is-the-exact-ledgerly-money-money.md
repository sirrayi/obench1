---
provenance: session:p1
confidence: 0.7
source: overseer:session/p1
added: 2026-11-05
valid_from: 2026-11-05T20:32:49Z
---
ledgerly: money is the exact ledgerly.money.Money (Decimal + currency); rates typed decimal.Decimal. Rounding is per package: invoices/billing/tax/reports/export ROUND_HALF_UP, fx/interest ROUND_HALF_EVEN, refunds ROUND_DOWN, and payouts ROUND_HALF_EVEN because AMENDMENTS/001 overrides MIGRATION.md. MoneyF/Rate must never reappear; ledgerly/util.round_money was removed. legacy/ is frozen and uses convert_float (float in/out).
