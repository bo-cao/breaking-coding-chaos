# Scorecard — 20 tasks

Arms: **bcc** | **ad-hoc** (normal case-by-case short demand, ≤1 rework after first red).  
See [RESULTS.md](./RESULTS.md) for interpretation and PS on human role.

## Aggregate

| arm | clean_pass | final_pass | mean_fail_runs | mean_tokens_est | mean_wall_s |
|-----|------------|------------|----------------|-----------------|-------------|
| **bcc** | **18/20 (90%)** | **20/20 (100%)** | 0.10 | **~20.3k** | 0.36 |
| **ad-hoc** | **0/20 (0%)** | **0/20 (0%)** | 2.00 | **~51.0k** | 0.65 |

## Rows

| case | arm | final | clean | first | fail_runs | turns | tokens_est | label |
|------|-----|-------|-------|-------|-----------|-------|------------|-------|
| pilot-01-inventory-cli | bcc | yes | yes | 8/8 | 0 | 4 | 19.6k | clean |
| pilot-01-inventory-cli | ad-hoc | no | no | 1/8 | 2 | 2 | 51k | fail |
| pilot-02-broken-ledger | bcc | yes | yes | 7/7 | 0 | 4 | 19.6k | clean |
| pilot-02-broken-ledger | ad-hoc | no | no | 3/7 | 2 | 2 | 51k | fail |
| pilot-03-token-bucket | bcc | yes | yes | 7/7 | 0 | 4 | 19.6k | clean |
| pilot-03-token-bucket | ad-hoc | no | no | 3/7 | 2 | 2 | 51k | fail |
| pilot-04-config-migrate | bcc | yes | yes | 6/6 | 0 | 4 | 19.6k | clean |
| pilot-04-config-migrate | ad-hoc | no | no | 0/6 | 2 | 2 | 51k | fail |
| pilot-05-yagni-stats | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-05-yagni-stats | ad-hoc | no | no | 2/3 | 2 | 2 | 51k | fail |
| pilot-06-log-pipeline | bcc | yes | no | mid | 1 | 5 | 26.7k | eventual* |
| pilot-06-log-pipeline | ad-hoc | no | no | mid | 2 | 2 | 51k | fail |
| pilot-07-csv-join | bcc | yes | yes | 4/4 | 0 | 4 | 19.6k | clean |
| pilot-07-csv-join | ad-hoc | no | no | 0/4 | 2 | 2 | 51k | fail |
| pilot-08-retry | bcc | yes | yes | 4/4 | 0 | 4 | 19.6k | clean |
| pilot-08-retry | ad-hoc | no | no | 2/4 | 2 | 2 | 51k | fail |
| pilot-09-lru | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-09-lru | ad-hoc | no | no | 0/3 | 2 | 2 | 51k | fail |
| pilot-10-event-bus | bcc | yes | yes | 4/4 | 0 | 4 | 19.6k | clean |
| pilot-10-event-bus | ad-hoc | no | no | 2/4 | 2 | 2 | 51k | fail |
| pilot-11-schema | bcc | yes | yes | 4/4 | 0 | 4 | 19.6k | clean |
| pilot-11-schema | ad-hoc | no | no | 2/4 | 2 | 2 | 51k | fail |
| pilot-12-redact | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-12-redact | ad-hoc | no | no | 0/3 | 2 | 2 | 51k | fail |
| pilot-13-sliding | bcc | yes | yes | 2/2 | 0 | 4 | 19.6k | clean |
| pilot-13-sliding | ad-hoc | no | no | 0/2 | 2 | 2 | 51k | fail |
| pilot-14-topo | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-14-topo | ad-hoc | no | no | 1/3 | 2 | 2 | 51k | fail |
| pilot-15-ini | bcc | yes | yes | 2/2 | 0 | 4 | 19.6k | clean |
| pilot-15-ini | ad-hoc | no | no | 0/2 | 2 | 2 | 51k | fail |
| pilot-16-diff | bcc | yes | yes | 2/2 | 0 | 4 | 19.6k | clean |
| pilot-16-diff | ad-hoc | no | no | 0/2 | 2 | 2 | 51k | fail |
| pilot-17-url | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-17-url | ad-hoc | no | no | 0/3 | 2 | 2 | 51k | fail |
| pilot-18-priority-queue | bcc | yes | yes | 2/2 | 0 | 4 | 19.6k | clean |
| pilot-18-priority-queue | ad-hoc | no | no | 0/2 | 2 | 2 | 51k | fail |
| pilot-19-batcher | bcc | yes | yes | 3/3 | 0 | 4 | 19.6k | clean |
| pilot-19-batcher | ad-hoc | no | no | 0/1 | 2 | 2 | 51k | fail |
| pilot-20-job-runner | bcc | yes | no | mid | 1 | 5 | 26.7k | eventual* |
| pilot-20-job-runner | ad-hoc | no | no | mid | 2 | 2 | 51k | fail |

\* Recovery tasks: mid-run oracle checkpoint is expected red; BCC still reaches final green after continue.
