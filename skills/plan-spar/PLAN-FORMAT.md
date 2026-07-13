# PLAN.md Format

Adapted from grill-with-docs PLAN-FORMAT for **plan-spar**.

`PLAN.md` is the **current executable coding plan only**. Not a glossary, not throughline progress.
plan-spar **locks** and spars this file; **clean-cut** executes it and trims completed items.
Both **update / 约减** so PLAN stays short.

Do **not** write coding plans into `plans.md` / `findings.md` / `progress.md`.

## Template

```markdown
# Plan: <task>
_Locked via plan-spar — <date or session>. Terms per CONTEXT.md._

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
