---
name: bcc-breaking-coding-chaos
description: >
  BCC main skill: dual-loop coding workflow (throughline → plan-spar → clean-cut)
  or quick status+next. Slash: /bcc-breaking-coding-chaos · chat: bcc:breaking-coding-chaos ·
  "run BCC" · "BCC status" · "what next BCC". Needs a real idea (1:1 implement).
argument-hint: "slash: /bcc-breaking-coding-chaos · chat: bcc:breaking-coding-chaos · [goal|status]"
metadata:
  short-description: "BCC main workflow"
---

# bcc-breaking-coding-chaos

**One main skill + three sub-skills.** This file is the only “big” entry; the three children own deep rules.

| Sub-skill | Role |
|-----------|------|
| [bcc-throughline](../bcc-throughline/SKILL.md) | Global map: `plans.md` / `progress.md` / `findings.md` only |
| [bcc-plan-spar](../bcc-plan-spar/SKILL.md) | After throughline: single `PLAN.md` align + review |
| [bcc-clean-cut](../bcc-clean-cut/SKILL.md) | After human APPROVE: minimal code + verify + writeback |

Internal notes (not separate slash skills): [references/SESSION.md](./references/SESSION.md), [references/WRITEBACK.md](./references/WRITEBACK.md).

**Prerequisite:** a **reasonably concrete idea**. BCC is **1:1 implement + control**, not ideation from zero.

---

## Two modes (this skill)

### Mode A — full chain

When user says run BCC / full flow / implement this idea end-to-end:

```text
1. bcc-throughline   (create/update cockpit — required first)
2. confirm next hardpoint with user
3. bcc-plan-spar     (hard: only after throughline)
4. human APPROVE → write .bcc/session.json (see references/SESSION.md)
5. bcc-clean-cut     (code + verify + mandatory writeback)
6. brief status + ask next hardpoint or stop
```

**Thin orchestration only** — open each child’s SKILL.md and follow it; do not re-copy grill/review/ladder text here.

### Mode B — user drives

User calls sub-skills directly. This main skill is optional.

### Quick status (built-in — not a separate skill)

When user only wants “where are we / what next” (or args `status`):

1. Read `plans.md`, `progress.md`, `findings.md`, `PLAN.md`, `.bcc/session.json` if present.  
2. Print short block:

```text
BCC status
  goal:     ...
  phase:    ...
  slice:    ...
  PLAN:     missing|draft|locked|complete
  session:  ...
  next:     /bcc-throughline | /bcc-plan-spar | /bcc-clean-cut | ask-user
  why:      <one sentence>
```

3. **Stop** — no grill, no code. If they say “do that next”, load that sub-skill.

| Condition | `next` |
|-----------|--------|
| No `plans.md` / empty goal | `/bcc-throughline` |
| Need align / lock PLAN | `/bcc-plan-spar` (only if throughline OK) |
| PLAN approved for code (session or chat) | `/bcc-clean-cut` |
| Unclear | `ask-user` + recommended default |

---

## Hard workflow rules (remind only)

1. **throughline before plan-spar**  
2. **One `PLAN.md`**, updated in place; global progress only in the three throughline files  
3. **Human APPROVE** before clean-cut (session file optional help)  
4. **Writeback** after clean-cut success is mandatory ([WRITEBACK.md](./references/WRITEBACK.md))  
5. Infer next step from docs + chat; **suggest** to user — no heavy formal state machine  

## What NOT to do

- Don't install or invent extra slash skills (`bcc-status`, bare `bcc`, etc.).  
- Don't implement product code in this skill except by loading **bcc-clean-cut**.  
- Don't plan-spar without throughline.  
