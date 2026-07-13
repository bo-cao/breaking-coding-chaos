# Benchmarks

Measure **project completion** under **BCC** vs **without_skill** (multi-turn short demand prompts only).  
Methodology is **inspired by** the public eval style in [planning-with-files `docs/evals.md`](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/evals.md) (objective checks, with/without arms, tokens/time) — **we do not run a planning-with-files comparison arm.**

Python-first. Pilot **6** cases, then expand toward **20**.  
**Project `AGENTS.md` stays empty** so the agent is not steered by repo-global instructions outside the skills under test.

---

## Publication rule (important)

**Do not publish full methodology detail, raw traces, or internal case keys until we jointly review the public write-up.**

After runs finish:

1. Align on **which numbers and narrative** go public (README / optional evals note).
2. Prefer **aggregates**: success rate, tokens, wall time, turns, ruff-level cleanliness.
3. Do **not** dump auto-APPROVE internals, full harness prompts, or spoiler solutions.

Internal scorecards may live under this tree during development; **public text is a separate decision.**  
No public claim of numbers until that review.

---

## Arms

| Arm | Setup |
|-----|--------|
| **BCC** | Four `bcc-*` skills loaded; dual-loop workflow; **auto-APPROVE** when the skill waits on implement gate |
| **without_skill** | No BCC skills; multi-turn **short demand** prompts only (continue / next slice / until done) |

Same model/runtime family per paired run (v1: Grok / local environment). Isolated workdir per arm × case.

---

## Success judgment (oracle-first, multi-metric)

Aligned with the spirit of pwf-style evals: **machine-checkable outcomes**, not vibe scores.  
**Do not reduce a run to a single “pass” bit** if there was rework after a red suite.

### Required outcome fields (every run)

| Field | Definition |
|-------|------------|
| **final_pass** | Last tree is oracle all-green within budget |
| **clean_pass** | **First** full oracle run was already all-green |
| **first_ok/total** | On first pytest: tests passed / collected |
| **fail_runs** | Count of oracle runs that were not all-green |
| **pytest_runs** | How many times the full oracle was run |
| **turns_to_green** | Steps until **first** all-green (`—` if never) |

### Success labels

| Label | Rule | Notes |
|-------|------|--------|
| **Clean success** | `clean_pass` ∧ `final_pass` | Preferred headline |
| **Eventual success** | `final_pass` ∧ ¬`clean_pass` | Recovered after red suite(s) — **report separately** |
| **Fail** | ¬`final_pass` | Budget hit or abandoned red |

**Rates per arm:**

- `clean_pass_rate` = clean successes / N  
- `eventual_pass_rate` = final_pass / N  
- Also: mean `fail_runs`, mean `turns_to_green`, tokens, wall, turns, ruff  

Example: first pytest `0/5`, later `5/5` → **eventual success**, **not** clean success.

### Secondary: process notes (BCC, optional)

File/transcript checks for internal analysis (publish only if we agree): progress trio, single living plan, writeback after slice.

### Not used as sole pass/fail

- LLM-as-judge freeform “quality” alone  
- “Looks done” without oracle  

---

## Tokens and efficiency

Record per run when the runtime exposes usage:

| Metric | Use |
|--------|-----|
| **Tokens** (in/out or total) | Cost; compare arms |
| **Wall time** | Latency |
| **Turns** | Interaction length |
| **ruff** (or agreed linter) on final Python | Cleanliness proxy |

### Narrative target (task design, not a guarantee)

Prefer cases where **without_skill** fails or **burns tokens on rework** (redo, thrash, re-ask, hallucinated APIs), while **BCC** finishes with a **green oracle** — so we can report **higher success** and, where measured, **equal or lower tokens to success** (or tokens-per-success).

Avoid only “easy one-shot” tasks where both arms pass cheaply (little separation).  
If a run has no token meter → record `n/a`, still report pass/time/turns.

---

## Case selection (difficulty filter)

Each case should be hard enough that **skill structure matters**:

| Prefer | Avoid |
|--------|--------|
| Multi-slice project (≥3 natural sub-tasks) | Single-file toy scripts |
| Constraints that pure short-demand thrashing breaks | Vague “build anything cool” |
| Spec + tests as source of truth | Open-ended vibe-only goals |
| ~1/3 of suite: **hard-stop recovery** then Continue | Only recovery with no oracle |
| BCC’s dual loop can own progress + one hard slice | Tasks that only need chat memory |

**Filter rule:** if pilot shows **both arms pass in one short session with similar tokens**, demote or harden the case before counting it in the 20.

---

## Scale and recovery

| Phase | Cases | Recovery share |
|-------|-------|----------------|
| Pilot | 6 | ~2 (~1/3) |
| Full target | 20 | ~6–7 (~1/3) |

Recovery protocol (high level): stop near mid progress → new session → only “continue the work in this directory” style demand → grade final oracle.

---

## Deliverables (v1)

| Artifact | Role |
|----------|------|
| This README | Public-safe protocol summary |
| `tasks/` (when added) | Per-case brief + oracle (internal detail as needed) |
| `scorecard.md` (when added) | Manual run log: arm × case × metrics |

No full auto harness required for v1; hand-run + table is enough.

---

## Status

- [x] Direction locked (arms, oracle pass, tokens, difficulty filter, empty `AGENTS.md`)
- [x] Pilot task briefs + oracles — see [`tasks/`](./tasks/)
- [x] Manual [`scorecard.md`](./scorecard.md) template
- [ ] Pilot runs
- [ ] Joint review of **public** result form
- [ ] Expand toward 20

**AGENTS.md:** keep **empty** in this repo (no project-level agent instructions that confound the skill comparison).

## Pilot map

| ID | Focus | Recovery |
|----|--------|----------|
| pilot-01 | Multi-slice inventory store | no |
| pilot-02 | Fix broken ledger + extend | no |
| pilot-03 | Spec-hard token bucket | no |
| pilot-04 | Config v1→v2 migrate | no |
| pilot-05 | YAGNI line stats | no |
| pilot-06 | Multi-stage log pipeline | **yes** |
