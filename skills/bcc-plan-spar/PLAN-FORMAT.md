# PLAN.md Format

Adapted from grill-with-docs PLAN-FORMAT for **bcc-plan-spar**.

`PLAN.md` is the **one** current executable coding plan (repo root by default).  
Not a glossary, not the global endeavor log.

- **Global** phases / hardpoint map / session history → only `plans.md` / `progress.md` / `findings.md`.  
- **No** per-slice PLAN file tree: when the active hardpoint changes, **rewrite this same `PLAN.md`**.  
- bcc-plan-spar locks/spars (only place to refine design).  
- bcc-clean-cut **executes**; may check off / drop *completed* checklist rows only — **no** mid-cut redesign of Goal/Approach/decisions. Keep short.

Do **not** write coding checklists into the throughline trio.

## Template

```markdown
# Plan: <task>
_Locked via bcc-plan-spar — <date or session>. Terms per CONTEXT.md._

## Goal
<one paragraph, ubiquitous language from CONTEXT.md>

## Approach
1. <concrete step>
2. <concrete step>

## Key decisions & tradeoffs
- <choice resolved in hardpoint — link ADR if any>

## Implementation checklist
- [ ] <code change + how to verify this item>

## Verification
- <commands, tests, manual checks for done>

## Risks / open questions
- <only genuinely open items>

## Out of scope
- <bounds established in hardpoint>
```

## Rules

- Prefer terms from `CONTEXT.md`. Missing term → update glossary first.
- Checklist items are implementation-ready.
- Mark complete **only after** implementation + verification (Cut phase).
- After items complete: **remove or collapse them** (约减); move narrative to throughline `progress.md`.
- Strip theory and long debate; optional spar log: `PLAN-REVIEW-LOG.md`.
