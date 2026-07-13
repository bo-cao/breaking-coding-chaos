# Tasks (20)

| ID | Name | Recovery |
|----|------|----------|
| pilot-01 … pilot-06 | original pilots | 06 yes |
| pilot-07-csv-join | CSV join | no |
| pilot-08-retry | Retry backoff | no |
| pilot-09-lru | LRU cache | no |
| pilot-10-event-bus | Event bus | no |
| pilot-11-schema | Schema validate | no |
| pilot-12-redact | Secret redact | no |
| pilot-13-sliding | Sliding window | no |
| pilot-14-topo | Topo sort | no |
| pilot-15-ini | INI roundtrip | no |
| pilot-16-diff | Line diff | no |
| pilot-17-url | URL parts | no |
| pilot-18-priority-queue | Priority queue | no |
| pilot-19-batcher | Batcher | no |
| pilot-20-job-runner | Job runner | **yes** |

## Arms

| arm | Meaning |
|-----|---------|
| **bcc** | BCC dual-loop skills |
| **ad-hoc** | Normal case-by-case agent use (short multi-turn demands; **≤1 rework** after first red) |

## Operator

1. Copy `scaffold/` + `oracle/tests` → workdir; keep project `AGENTS.md` empty.  
2. Run **bcc** or **ad-hoc** per protocol.  
3. Log every full pytest into scorecard (`clean` vs `final`).  
4. Tokens: use runtime meter if available; else estimate formula in suite scripts.

See `../scorecard.md` and `../RESULTS_PILOT.md`.
