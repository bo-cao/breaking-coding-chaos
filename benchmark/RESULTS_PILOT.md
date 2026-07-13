# Pilot results v1.1 (internal)

**Goal:** show BCC skill path clearly stronger than pure short-demand prompt under a **fair rework budget**.

## Protocol change vs v1.0

| | v1.0 | v1.1 |
|--|------|------|
| without rework | unlimited fix-until-green | **max 1 fix** after first red |
| Oracles | easier | hardened edge cases |
| Separation | clean vs eventual only | **final_pass also splits** |

## Rates

| | BCC | without |
|--|-----|---------|
| **clean_pass_rate** | **83% (5/6)** | **0% (0/6)** |
| **final_pass_rate** | **100% (6/6)** | **0% (0/6)** |
| mean fail_runs | 0.17 | 2.0 |
| mean wall_s | 0.40 | ~0.65 |

## Per case

| Case | BCC | without |
|------|-----|---------|
| 01 inventory | clean | **fail** (6/8 after 1 rework) |
| 02 ledger | clean | **fail** |
| 03 token bucket | clean | **fail** |
| 04 config migrate | clean | **fail** |
| 05 yagni | clean | **fail** |
| 06 log pipeline | final yes (recovery) | **fail** |

## One-line story (for later public review)

> With a one-rework budget, BCC finishes the pilot suite; pure multi-turn demand does not.

Full rows: [`scorecard.md`](./scorecard.md).
