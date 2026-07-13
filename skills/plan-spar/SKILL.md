---
name: plan-spar
description: >
  Align one hard slice and lock a lean PLAN.md under breaking-coding-chaos:
  interview, CONTEXT.md and ADRs, auto-lock then update/trim PLAN, adversarial
  plan review, human APPROVE or amend. Does NOT implement code — after APPROVE
  hand off to clean-cut. Use for /plan-spar, new slice, "对齐并锁 PLAN", spar
  the plan. Inspired by grill-with-docs + domain-modeling; re-encapsulated
  under our name.
argument-hint: "[topic] [grill_rounds=N] [rounds=N] [review=self|off]"
---

# plan-spar

**Job:** make the coding contract solid — align → **lock / update / 约减 `PLAN.md`** → spar → **human gate**.

**Not this skill:** writing product code. That is **`clean-cut`** (ponytail ladder).

**Deep source:**

| Phase | Upstream |
|-------|----------|
| Align + CONTEXT + ADR + lock PLAN | grill-with-docs Act 1 + domain-modeling |
| Spar | grill-with-docs Act 2 |

**Formats:** [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), [ADR-FORMAT.md](./ADR-FORMAT.md), [PLAN-FORMAT.md](./PLAN-FORMAT.md).

**throughline** = global progress visibility/adjustment. **clean-cut** = implement PLAN.

---

## Tunables

| Arg | Default | Meaning |
|-----|---------|---------|
| `grill_rounds` | `12` | Soft cap on align Q&A turns |
| `rounds` | `3` | Max spar rounds before human breaks deadlock |
| `review` | `self` | `self` = agent critic; `off` = skip spar, still ask human before handoff |
| `PLAN_FILE` | `PLAN.md` | Coding brief path |

Echo: `plan-spar · topic=… · grill_rounds=12 · rounds=3 · review=self`

---

## When to start a **new** plan-spar

Each new slice / hard problem → new invoke:

1. Read throughline trio if present.  
2. Read `CONTEXT.md`, ADRs, code as needed.  
3. **Auto-lock or refresh `PLAN.md` for this slice.**  
4. Spar → human gate.  
5. On **APPROVE** → hand off to **`clean-cut`** (do not implement here).  
6. Keep **update + 约减** PLAN so it stays short (not a diary).

---

## Artifact separation

| File | Role |
|------|------|
| `CONTEXT.md` | Glossary only — assists PLAN |
| `docs/adr/*` | Hard-to-reverse decisions |
| **`PLAN.md`** | Living coding brief — lock, update, reduce |
| throughline trio | Global cockpit only |

---

## Phase 0 — Scope the slice

- Name the hard problem (user topic or next from `plans.md`).  
- Resume: read PLAN, trim already-done items toward progress.  
- New slice: do not pile infinite done history into PLAN.

---

## Phase 1 — Align + lock PLAN

### Interview (grill Act 1)

- One question at a time; recommended answer; facts from code; decisions to user.  
- Cap `grill_rounds` → summarize; lock now / raise / stop.

### Domain

- Update **`CONTEXT.md` inline**; ADRs only when hard to reverse · surprising · trade-off.  
- Cross-check claims against code.

### Clear enough → **auto-lock `PLAN.md`**

Goal, approach, decisions, checklist + verification, out of scope (PLAN-FORMAT).

Announce: `PLAN.md locked via plan-spar for <slice>.`

**No product code in plan-spar.**

### PLAN hygiene: update + 约减

| Action | Meaning |
|--------|---------|
| Update | Reality, constraints, checklist truth |
| 约减 | Drop speculative/done bulk; only remaining contract |
| Never | Diary, design essay, throughline dump |

Locked ≠ frozen — active contract, kept short.

---

## Phase 2 — Spar + human gate

Critic stance; one-line fixes; `VERDICT: APPROVED` | `VERDICT: REVISE`.

Loop ≤ `rounds`; REVISE → update/trim PLAN; cap → human tie-break. Never fake APPROVED.

Human gate:

> **APPROVE** → run **clean-cut** · **amend** · **stop**

- Amend → fix PLAN/CONTEXT/ADR → re-spar if material.  
- APPROVE → **load `clean-cut`** (or tell user `/clean-cut`).  
- stop → optional throughline note; exit.

Optional log: `PLAN-REVIEW-LOG.md`.

---

## Handoff to clean-cut

After APPROVE, plan-spar’s job ends for this slice’s *planning* track:

```text
plan-spar (done) → clean-cut (implement + verify + PLAN 约减 + throughline writeback)
```

If user says “skip spar, implement” with an already-locked PLAN → go straight to clean-cut.

---

## Invocation

| How | Example |
|-----|---------|
| Skill | `/plan-spar` · `/plan-spar auth grill_rounds=8` |
| Chat | "plan-spar", "对齐并锁 PLAN", "spar the plan" |

## Hard rules

1. New slice locks/refreshes PLAN.  
2. Update + 约减 PLAN; never grow forever.  
3. CONTEXT = glossary; checklist only in PLAN.  
4. **Never implement product code here** — clean-cut only.  
5. throughline trio ≠ coding brief.  
6. Bounded rounds.

## What NOT to do

- Don't implement “just a little” after APPROVE inside plan-spar.  
- Don't require a separate hardpoint skill.  
- Don't dump micro decisions into throughline.
