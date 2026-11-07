---
provenance: review:session:p1
confidence: 0.6
source: overseer:session/p1#e529
added: 2026-11-05
cues: ledgerly, money, decimal, amendments
valid_from: 2026-11-05T20:50:28Z
---
ledgerly: money is exact Money/Decimal in all packages except legacy/, which is deliberately left on floats (convert_float still returns floats). MIGRATION.md holds the migration rules; AMENDMENTS/ decisions override it — payouts round HALF_EVEN. The finished repo state is what hidden checks grade, so teammate-added modules must adopt the same rules.
