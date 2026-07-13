---
name: breaking-coding-chaos
description: >
  Human-in-the-loop dual-loop suite: throughline for progress visibility and
  adjustment; plan-spar to lock and spar PLAN.md; clean-cut to implement the
  brief with a minimal diff. Use for /breaking-coding-chaos, break coding
  chaos, or ship an idea step by step. Routes to throughline, plan-spar, and
  clean-cut.
argument-hint: "[goal or topic]"
---

# breaking-coding-chaos

**If you have a reasonable idea, ship it step by step — without losing the plot.**

| Skill | When |
|-------|------|
| [throughline](../throughline/SKILL.md) | See progress, adjust the endeavor map |
| [plan-spar](../plan-spar/SKILL.md) | Align slice → lock/update/trim PLAN → spar → human APPROVE |
| [clean-cut](../clean-cut/SKILL.md) | Implement PLAN with minimal code + verify (**ponytail ladder**) |

## Dual loop

```text
throughline                    plan-spar                 clean-cut
─────────────────────          ─────────────────         ──────────────
plans / progress / findings    CONTEXT · ADR · PLAN      min code + verify
"Where are we? Adjust."        lock → spar ⇄ you         (ponytail ladder)
         ▲                            │                        │
         │                            └── APPROVE ─────────────┘
         └──────────────── writeback after clean-cut ──────────┘
```

## Entry routine

1. **throughline** — trio current; user adjusts map.  
2. Per slice: **plan-spar** until APPROVE.  
3. **clean-cut** — implement + verify + trim PLAN + writeback.  
4. User picks next slice or stop.

## Routing

| Intent | Action |
|--------|--------|
| Status / resume / reprioritize | throughline |
| Align / lock / review PLAN | plan-spar |
| Implement approved PLAN | clean-cut |
| Full suite | this skill: throughline → plan-spar → clean-cut loop |
| Pure discussion | talk only |
| One-line fix | optional light clean-cut or raw edit |

## Artifacts

| File | Owner |
|------|--------|
| `plans.md` `progress.md` `findings.md` | throughline |
| `CONTEXT.md` `docs/adr/*` `PLAN.md` (lock/spar) | plan-spar |
| `PLAN.md` (complete items + 约减 during ship) | clean-cut (with plan-spar ownership of contract) |

## HITL gates

1. Adjust throughline map.  
2. plan-spar: answer questions; **APPROVE** before code.  
3. After clean-cut: inspect cockpit; next plan-spar or stop.

## What NOT to do

- Don't implement inside plan-spar.  
- Don't clean-cut without a real PLAN (send to plan-spar).  
- Don't freestyle against the three skill bodies.
