# Scorecard (manual / semi-manual)

**Do not publish raw rows until joint review of public narrative.**

Runtime: Grok / local · Arms: `bcc` | `without`

## Metric definitions

| Column | Meaning |
|--------|---------|
| **final_pass** | Oracle all-green on the **last** graded tree (within turn/time cap). Budget exhausted + red → `no`. |
| **clean_pass** | **Yes** only if the **first** full oracle run was already all-green (no failed pytest round before success). |
| **pytest_runs** | How many times the full oracle was executed. |
| **fail_runs** | How many of those runs were **not** all-green. |
| **first_ok/total** | On the **first** pytest run: `passed/collected` (e.g. `0/5`, `5/5`). |
| **turns_to_green** | Demand/structured steps until **first** all-green; `—` if never green. |
| **turns** | Total steps in the run (may continue after green for cleanup; usually == turns_to_green). |
| **tokens** | Usage if available; else `n/a`. |
| **wall_s** | Wall clock for the arm run (seconds). |
| **ruff_issues** | `ruff check` issue count on final tree (`0` if clean / tool missing note in notes). |

### How to read success (do not collapse to one bit)

| Label | Rule |
|-------|------|
| **Clean success** | `clean_pass=yes` ∧ `final_pass=yes` |
| **Eventual success** | `final_pass=yes` ∧ `clean_pass=no` (rework path — **not** the same as clean) |
| **Fail** | `final_pass=no` |

Headline rates to compute per arm:

- **clean_pass_rate** = clean successes / cases  
- **eventual_pass_rate** = final_pass yes / cases  
- **mean fail_runs**, **mean turns_to_green** (among eventual+clean), **mean wall_s**, **mean tokens**

---

## Pilot rows

| case_id | arm | final_pass | clean_pass | first_ok/total | fail_runs | pytest_runs | turns_to_green | turns | tokens | wall_s | ruff_issues | notes |
|---------|-----|------------|------------|----------------|-----------|-------------|----------------|-------|--------|--------|-------------|-------|
| pilot-01 | bcc | yes | **yes** | 5/5 | 0 | 1 | 4 | 4 | n/a | 0.42 | 0 | structured path; single grade after implement |
| pilot-01 | without | yes | **no** | 0/5 | 1 | 2 | 5 | 5 | n/a | 1.13 | 0 | **eventual only** — first suite FFFFF, then rework to 5/5 |
| pilot-02 | bcc | | | | | | | | | | | |
| pilot-02 | without | | | | | | | | | | | |
| pilot-03 | bcc | | | | | | | | | | | |
| pilot-03 | without | | | | | | | | | | | |
| pilot-04 | bcc | | | | | | | | | | | |
| pilot-04 | without | | | | | | | | | | | |
| pilot-05 | bcc | | | | | | | | | | | |
| pilot-05 | without | | | | | | | | | | | |
| pilot-06 | bcc | | | | | | | | | | | |
| pilot-06 | without | | | | | | | | | | | |

## Caps (default)

- Max **40 turns** or **30 minutes** wall (first hit → `final_pass=no` if still red).
- Auto-APPROVE phrase for BCC implement gate: `APPROVE IMPLEMENT` (harness-only).
- After each material implement turn, run full oracle and log `first_ok/total` / fail_runs.

## Aggregate (fill as pilots complete)

| arm | clean_pass_rate | eventual_pass_rate | mean_fail_runs | mean_turns_to_green | mean_wall_s | mean_tokens |
|-----|-----------------|--------------------|----------------|---------------------|-------------|-------------|
| bcc | 1/1 (pilot-01) | 1/1 | 0 | 4 | 0.42 | n/a |
| without | 0/1 (pilot-01) | 1/1 | 1 | 5 | 1.13 | n/a |

**Interpretation (pilot-01 only, internal):** both arms eventually green, but without is **not** a clean success — it required a failed suite + rework.
