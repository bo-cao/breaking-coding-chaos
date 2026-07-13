---
name: clean-cut
description: >
  Minimal implementation against a locked PLAN.md under breaking-coding-chaos.
  YAGNI ladder: reuse repo, stdlib, native, installed deps, one line, then
  minimum that works; then verify against PLAN and trim completed checklist
  items. Use after plan-spar APPROVE, or when the user says clean-cut, implement
  PLAN, ship the brief, minimal diff, or /clean-cut. Inspired by ponytail
  coding ladder only — re-encapsulated under our name. Not for alignment or
  plan review (that is plan-spar).
argument-hint: "[lite|full|ultra]"
---

# clean-cut

**Job:** ship the **shortest correct code** that satisfies the active `PLAN.md`, then verify and 约减 the checklist.

**Deep source:** `ponytail` SKILL.md (coding ladder only — not review/audit family).  
**Does not:** interview the user for domain design, write ADRs, or adversarial-review the plan — do that in **`plan-spar`** first.

## Preconditions

1. Prefer a **human-approved** (or user-skipped-spar) `PLAN.md` from plan-spar.  
2. Read `PLAN.md`, `CONTEXT.md`, relevant ADRs, and **trace the real code flow** before editing.  
3. If PLAN is missing / draft-only / clearly unaligned: stop and send user to **plan-spar**.

## Intensity (default **full**)

| Level | Behavior |
|-------|----------|
| **lite** | Build what PLAN asks; name a lazier alternative in one line. |
| **full** | Ladder enforced. Shortest correct diff. Default. |
| **ultra** | YAGNI extremist; challenge extra PLAN items in the same breath if they look speculative. |

Echo: `clean-cut · full · PLAN.md`

Off only if user says stop clean-cut / normal mode for coding style (suite may still own process).

---

## Before the ladder

- Read every file the change touches; end-to-end flow.  
- **Bug fix = root cause**, not symptom — one fix where all callers route.  
- Ladder shortens the **solution**, never the **reading**.

## The ladder (stop at first rung that holds)

1. Does this need to exist at all? (YAGNI)  
2. Already in this codebase? Reuse.  
3. Stdlib?  
4. Native platform feature?  
5. Already-installed dependency? Never add a dep for a few lines.  
6. One line?  
7. Only then: minimum code that works.

## Rules

- No unrequested abstractions (interface-for-one, factory-for-one, config-for-never).  
- No scaffolding “for later”.  
- Deletion over addition when safe. Fewest files. Shortest **correct** diff.  
- Equal-size options → pick edge-correct one.  
- Deliberate ceilings: `# bcc: <ceiling>; upgrade when <condition>`.

## Never simplify away

Trust-boundary validation, data-loss handling, security, a11y basics, anything PLAN/user explicitly requires. Never lazy about understanding.

## Verify + PLAN 约减

- Run checks from `PLAN.md` Verification + checklist.  
- Mark items complete **only after** implement + verify.  
- Non-trivial logic: one minimal runnable check if none exist (no test framework sprawl).  
- **约减 `PLAN.md`:** drop finished bulk; keep only remaining work (history → throughline `progress.md` when suite active).

## Output

Code first. At most a few short lines: skipped / add when.  
Pattern: `done → skipped: X, add when Y` unless user asked for a full report.

## Close

**Pass:** trim PLAN; if suite mode, throughline writeback (`progress.md`, sparse `plans.md` / `findings.md`); offer next **plan-spar** slice or stop.

**Fail:** log error; do not repeat identical failure (3-strike then escalate); if brief is wrong → **plan-spar** to revise PLAN, not silent scope creep in clean-cut.

## Invocation

| How | Example |
|-----|---------|
| After plan-spar | User APPROVE → agent loads **clean-cut** |
| Skill | `/clean-cut` · `/clean-cut ultra` |
| Chat | "clean-cut", "按 PLAN 最小实现", "implement the brief" |

## Hard rules

1. PLAN is the contract — do not invent scope.  
2. Read fully, then climb the ladder.  
3. No plan-review theater here — that is plan-spar.  
4. throughline trio is not the coding brief.

## What NOT to do

- Don't re-open unbounded product design.  
- Don't pull whole-repo audit skills.  
- Don't implement without reading PLAN.
