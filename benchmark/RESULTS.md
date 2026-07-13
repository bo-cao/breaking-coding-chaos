# Evaluation results (reference)

Controlled comparison of **breaking-coding-chaos (BCC)** against **ad-hoc** agent use on a **20-task** Python suite with **pytest oracles**.

## Design (summary)

| Item | Setting |
|------|---------|
| Tasks | 20 multi-constraint / multi-slice engineering tasks (stdlib Python) |
| Success | Machine-checked: full oracle green |
| **BCC** | Dual-loop skill suite: throughline → plan-spar → implement gate → clean-cut |
| **ad-hoc** | Normal **case-by-case** agent practice: short multi-turn demands only; **≤1 rework** after first failed oracle |
| Metrics | Clean pass (first oracle green), final pass, fail_runs, estimated tokens |

This framing stresses **reliable completion under a realistic interaction budget**, not unlimited “fix forever” thrashing.

## Headline results

| Metric | **BCC** | **ad-hoc** (case-by-case) |
|--------|---------|---------------------------|
| **Clean pass rate** (first full oracle green) | **90%** (18/20) | **0%** (0/20) |
| **Final pass rate** (within rework budget) | **100%** (20/20) | **0%** (0/20) |
| Mean failed oracle rounds | **0.10** | **2.00** |
| Mean tokens (estimated) | **~20.3k** | **~51.0k (~2.5×)** |

**Takeaway:** Under the same oracle standard and a one-rework cap on ad-hoc chat, BCC **completes the suite** with mostly first-try greens and **substantially lower estimated token cost**. Ad-hoc short-demand interaction does not reach final green within budget on these tasks.

Row-level data: [scorecard.md](./scorecard.md). Task definitions: [tasks/](./tasks/).

## Why this favors a control-plane skill

1. **Plan-then-cut reduces attention** on one living brief, reducing partial implementations that fail edge-case oracles.  
2. **Global progress files** support multi-slice and recovery-style work without relying on chat memory alone.  
3. **Human implement gates** (see PS) keep coding aligned with the locked plan before large diffs.  
4. **Ad-hoc case-by-case prompting** optimizes for the next utterance, not for full-spec closure under a hard rework limit—hence zero final passes here.

## PS — Role of “human” in the evaluation

In this evaluation, **human-in-the-loop decisions (including implement APPROVE) were enacted by agent subagents**, not by live human operators at the keyboard. Subagents followed a fixed policy (e.g. approve when the plan was locked and ready for clean-cut). Results therefore measure the **skill workflow + automated gate policy**, not a study of diverse human reviewers.

Tokens are **estimates** when no runtime meter was available (failed/rework paths penalized). Suite execution was dual-arm and oracle-driven; interpret as a **controlled benchmark**, not a multi-vendor production A/B farm.
