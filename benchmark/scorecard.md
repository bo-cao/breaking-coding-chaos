# Scorecard (manual / semi-manual)

**Do not publish raw rows until joint review of public narrative.**

Runtime: Grok workspace (scripted dual-arm simulation) · Arms: `bcc` | `without`  
Tokens: **n/a** on this path (no usage meter).

## Metric definitions

| Column | Meaning |
|--------|---------|
| **final_pass** | Last tree oracle all-green within budget |
| **clean_pass** | First full oracle run already all-green (**no** prior red suite) |
| **first_ok/total** | First pytest: passed/collected (approx) |
| **fail_runs** | Oracle runs that were not all-green |
| **pytest_runs** | Full oracle executions |
| **turns_to_green** | Steps until first all-green |
| **turns** | Total steps logged |
| **wall_s** | Wall seconds |
| **ruff_issues** | Final `ruff check` (0 if clean / not run noted) |

| Label | Rule |
|-------|------|
| **Clean success** | clean_pass ∧ final_pass |
| **Eventual success** | final_pass ∧ ¬clean_pass |
| **Fail** | ¬final_pass |

---

## Pilot rows (all 6)

| case_id | arm | final_pass | clean_pass | first_ok/total | fail_runs | pytest_runs | turns_to_green | turns | tokens | wall_s | ruff | label | notes |
|---------|-----|------------|------------|----------------|-----------|-------------|----------------|-------|--------|-------|------|-------|-------|
| pilot-01 | bcc | yes | **yes** | 5/5 | 0 | 1 | 4 | 4 | n/a | 0.42 | 0 | clean | inventory store |
| pilot-01 | without | yes | **no** | 0/5 | 1 | 2 | 5 | 5 | n/a | 1.13 | 0 | eventual | thrash then fix |
| pilot-02 | bcc | yes | **yes** | 5/5 | 0 | 1 | 4 | 4 | n/a | 0.39 | 0 | clean | fix ledger+statement |
| pilot-02 | without | yes | **no** | 3/5 | 2 | 3 | 3 | 3 | n/a | 0.91 | 0 | eventual | multi red rounds |
| pilot-03 | bcc | yes | **yes** | 5/5 | 0 | 1 | 3 | 3 | n/a | 0.32 | 0 | clean | token bucket |
| pilot-03 | without | yes | **no** | 3/5 | 1 | 2 | 2 | 2 | n/a | 0.61 | 0 | eventual | missing clock first |
| pilot-04 | bcc | yes | **yes** | 4/4 | 0 | 1 | 3 | 3 | n/a | 0.35 | 0 | clean | config migrate |
| pilot-04 | without | yes | **no** | 3/4 | 1 | 2 | 2 | 2 | n/a | 0.64 | 0 | eventual | missed v2 reject |
| pilot-05 | bcc | yes | **yes** | 3/3 | 0 | 1 | 3 | 3 | n/a | 0.32 | 0 | clean | yagni minimal |
| pilot-05 | without | yes | **no** | 2/3 | 1 | 2 | 2 | 2 | n/a | 0.66 | 0 | eventual | overbuild then trim |
| pilot-06 | bcc | yes | **no** | 0/* | 1 | 2 | 5 | 5 | n/a | 0.73 | 0 | eventual | recovery: mid-grade red then finish |
| pilot-06 | without | yes | **no** | 0/* | 2 | 3 | 3 | 3 | n/a | 1.11 | 0 | eventual | recovery thrash more fail_runs |

\* pilot-06 first grade is intentional mid-pipeline checkpoint (imports/tests incomplete).

---

## Aggregate (pilot-01 … pilot-06)

| arm | N | clean_pass_rate | eventual_pass_rate | final_pass_rate | mean_fail_runs | mean_turns_to_green | mean_wall_s | mean_tokens |
|-----|---|-----------------|--------------------|-----------------|----------------|---------------------|-------------|-------------|
| **bcc** | 6 | **5/6 (83%)** | 6/6 (100%) | 6/6 | **0.17** | 3.7 | **0.42** | n/a |
| **without** | 6 | **0/6 (0%)** | 6/6 (100%) | 6/6 | **1.33** | 2.8 | **0.84** | n/a |

### Readout (internal)

1. **Do not say “both 100% pass”** without splitting clean vs eventual.  
2. **BCC** dominates **clean_pass** (5/6); only recovery case is eventual by design (mid-stop grade).  
3. **without** is always **eventual** here: red suites + rework, ~**2× wall**, ~**8× fail_runs**.  
4. **turns_to_green** can look lower for without when thrash steps are coarse; prefer **fail_runs + clean_pass + wall** as separation.  
5. **Tokens** still unmeasured on this harness — next runs should attach usage if the runtime exposes it.  
6. Not a public claim until joint review; method is scripted dual-arm in-workspace, not a third-party agent farm.

## Caps

- Max 40 turns / 30 min → final_pass=no if still red.  
- BCC auto-APPROVE: `APPROVE IMPLEMENT`.  
- Grade after material implements; log every full oracle run.
