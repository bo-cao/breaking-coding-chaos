# Scorecard (20 cases · v1.2)

**Internal only — public write-up requires joint review.**

Arms:
- **bcc** — dual-loop skill suite (throughline → plan-spar → auto APPROVE → clean-cut)
- **ad-hoc** — normal case-by-case agent use: short multi-turn demands, **max 1 rework** after first red oracle

Tokens are **estimates** (no runtime meter): thrash/fail paths pay rework penalties.

## Aggregate

| arm | clean_pass_rate | final_pass_rate | mean_fail_runs | mean_tokens_est | mean_wall_s |
|-----|-----------------|-----------------|----------------|-----------------|-------------|
| **bcc** | **18/20 (90%)** | **20/20 (100%)** | 0.10 | **20,310** | 0.36 |
| **ad-hoc** | **0/20 (0%)** | **0/20 (0%)** | 2.00 | **51,000** | 0.65 |

Token ratio (ad-hoc / bcc mean est.): **2.51x**

## All rows

| case | arm | final | clean | first | fail_runs | turns | tokens_est | wall_s | label |
|------|-----|-------|-------|-------|-----------|-------|------------|--------|-------|
| pilot-01-inventory-cli | bcc | yes | yes | 8/8 | 0 | 4 | 19,600 | 0.34 | clean |
| pilot-01-inventory-cli | ad-hoc | no | no | 1/8 | 2 | 2 | 51,000 | 0.64 | fail |
| pilot-02-broken-ledger | bcc | yes | yes | 7/7 | 0 | 4 | 19,600 | 0.31 | clean |
| pilot-02-broken-ledger | ad-hoc | no | no | 3/7 | 2 | 2 | 51,000 | 0.62 | fail |
| pilot-03-token-bucket | bcc | yes | yes | 7/7 | 0 | 4 | 19,600 | 0.3 | clean |
| pilot-03-token-bucket | ad-hoc | no | no | 3/7 | 2 | 2 | 51,000 | 0.6 | fail |
| pilot-04-config-migrate | bcc | yes | yes | 6/6 | 0 | 4 | 19,600 | 0.37 | clean |
| pilot-04-config-migrate | ad-hoc | no | no | 0/6 | 2 | 2 | 51,000 | 0.67 | fail |
| pilot-05-yagni-stats | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.38 | clean |
| pilot-05-yagni-stats | ad-hoc | no | no | 2/3 | 2 | 2 | 51,000 | 0.63 | fail |
| pilot-06-log-pipeline | bcc | yes | no | 0/1 | 1 | 5 | 26,700 | 0.76 | eventual |
| pilot-06-log-pipeline | ad-hoc | no | no | 0/1 | 2 | 2 | 51,000 | 0.81 | fail |
| pilot-07-csv-join | bcc | yes | yes | 4/4 | 0 | 4 | 19,600 | 0.31 | clean |
| pilot-07-csv-join | ad-hoc | no | no | 0/4 | 2 | 2 | 51,000 | 0.64 | fail |
| pilot-08-retry | bcc | yes | yes | 4/4 | 0 | 4 | 19,600 | 0.29 | clean |
| pilot-08-retry | ad-hoc | no | no | 2/4 | 2 | 2 | 51,000 | 0.61 | fail |
| pilot-09-lru | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.3 | clean |
| pilot-09-lru | ad-hoc | no | no | 0/3 | 2 | 2 | 51,000 | 0.61 | fail |
| pilot-10-event-bus | bcc | yes | yes | 4/4 | 0 | 4 | 19,600 | 0.32 | clean |
| pilot-10-event-bus | ad-hoc | no | no | 2/4 | 2 | 2 | 51,000 | 0.64 | fail |
| pilot-11-schema | bcc | yes | yes | 4/4 | 0 | 4 | 19,600 | 0.33 | clean |
| pilot-11-schema | ad-hoc | no | no | 2/4 | 2 | 2 | 51,000 | 0.64 | fail |
| pilot-12-redact | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.33 | clean |
| pilot-12-redact | ad-hoc | no | no | 0/3 | 2 | 2 | 51,000 | 0.63 | fail |
| pilot-13-sliding | bcc | yes | yes | 2/2 | 0 | 4 | 19,600 | 0.34 | clean |
| pilot-13-sliding | ad-hoc | no | no | 0/2 | 2 | 2 | 51,000 | 0.69 | fail |
| pilot-14-topo | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.32 | clean |
| pilot-14-topo | ad-hoc | no | no | 1/3 | 2 | 2 | 51,000 | 0.67 | fail |
| pilot-15-ini | bcc | yes | yes | 2/2 | 0 | 4 | 19,600 | 0.33 | clean |
| pilot-15-ini | ad-hoc | no | no | 0/2 | 2 | 2 | 51,000 | 0.6 | fail |
| pilot-16-diff | bcc | yes | yes | 2/2 | 0 | 4 | 19,600 | 0.32 | clean |
| pilot-16-diff | ad-hoc | no | no | 0/2 | 2 | 2 | 51,000 | 0.6 | fail |
| pilot-17-url | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.3 | clean |
| pilot-17-url | ad-hoc | no | no | 0/3 | 2 | 2 | 51,000 | 0.59 | fail |
| pilot-18-priority-queue | bcc | yes | yes | 2/2 | 0 | 4 | 19,600 | 0.3 | clean |
| pilot-18-priority-queue | ad-hoc | no | no | 0/2 | 2 | 2 | 51,000 | 0.6 | fail |
| pilot-19-batcher | bcc | yes | yes | 3/3 | 0 | 4 | 19,600 | 0.31 | clean |
| pilot-19-batcher | ad-hoc | no | no | 0/1 | 2 | 2 | 51,000 | 0.74 | fail |
| pilot-20-job-runner | bcc | yes | no | 0/1 | 1 | 5 | 26,700 | 0.73 | eventual |
| pilot-20-job-runner | ad-hoc | no | no | 0/1 | 2 | 2 | 51,000 | 0.8 | fail |

## Caps

- ad-hoc: ≤1 rework after first red; still red → final_pass=no
- recovery cases (06, 20): mid-grade then one continue for bcc; ad-hoc one continue only

