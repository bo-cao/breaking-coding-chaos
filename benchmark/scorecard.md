# Scorecard (manual / semi-manual)

**Do not publish raw rows until joint review of public narrative.**

Runtime: Grok / local · Arms: `bcc` | `without` · Pass = oracle all-green.

| case_id | arm | pass | tokens | wall_s | turns | ruff_issues | notes |
|---------|-----|------|--------|--------|-------|-------------|-------|
| pilot-01 | bcc | yes | n/a | 0.42 | 4 | 0 | throughline+PLAN+clean-cut; pytest 5/5; runs/pilot-01/bcc |
| pilot-01 | without | yes | n/a | 1.13 | 5 | 0 | multi-turn thrash then fix; first pytest 0/5; final 5/5; runs/pilot-01/without |
| pilot-02 | bcc | | | | | | |
| pilot-02 | without | | | | | | |
| pilot-03 | bcc | | | | | | |
| pilot-03 | without | | | | | | |
| pilot-04 | bcc | | | | | | |
| pilot-04 | without | | | | | | |
| pilot-05 | bcc | | | | | | |
| pilot-05 | without | | | | | | |
| pilot-06 | bcc | | | | | | |
| pilot-06 | without | | | | | | |

## Caps (default)

- Max **40 turns** or **30 minutes** wall (first hit → fail if oracle red).
- Auto-APPROVE phrase for BCC implement gate: `APPROVE IMPLEMENT` (harness-only).

## Aggregate (fill after pilot)

| arm | pass_rate | avg_tokens | avg_wall_s | avg_turns | avg_ruff |
|-----|-----------|------------|------------|-----------|----------|
| bcc | | | | | |
| without | | | | | |
