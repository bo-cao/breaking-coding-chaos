# Pilot results snapshot (internal)

See [`scorecard.md`](./scorecard.md) for full definitions.

## Quick table

| Case | BCC | without |
|------|-----|---------|
| 01 inventory | clean | eventual (0/5 → 5/5) |
| 02 ledger | clean | eventual (3/5, 2 fail runs) |
| 03 token bucket | clean | eventual |
| 04 config migrate | clean | eventual |
| 05 yagni stats | clean | eventual (bloat then trim) |
| 06 log pipeline (recovery) | eventual* | eventual (more fail_runs) |

\* Mid-session oracle grade required by recovery protocol.

## Rates

| | BCC | without |
|--|-----|---------|
| clean_pass_rate | **83% (5/6)** | **0% (0/6)** |
| final_pass_rate | 100% | 100% |
| mean fail_runs | 0.17 | 1.33 |
| mean wall_s | 0.42 | 0.84 |

Raw JSON (local, gitignored tree): `runs/all-pilot-results.json`.
