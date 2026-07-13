# Evaluation results

Controlled comparison of **breaking-coding-chaos (BCC)** against **ad-hoc** agent use on a **20-task** Python suite with **pytest oracles**.

## Design

| Item | Setting |
|------|---------|
| Tasks | 20 multi-constraint / multi-slice engineering tasks (stdlib Python) |
| Success | Machine-checked: full oracle green |
| **BCC** | Dual-loop skill suite: throughline → plan-spar → implement gate → clean-cut |
| **ad-hoc** | Everyday case-by-case prompting: raise each need as it appears, write a prompt, solve it—**without** layered plan management; **≤1 rework** after first failed oracle |
| Metrics | Clean pass, final pass, fail_runs, tokens |

## Headline results

[![Clean pass](https://img.shields.io/badge/Clean_pass-90%25-brightgreen)](./RESULTS.md)
[![Final pass](https://img.shields.io/badge/Final_pass-100%25-success)](./RESULTS.md)

| Metric | **BCC** | **ad-hoc** |
|--------|---------|------------|
| **Clean pass rate** | **90%** (18/20) | **0%** (0/20) |
| **Final pass rate** | **100%** (20/20) | **0%** (0/20) |
| Mean failed oracle rounds | **0.10** | **2.00** |
| Mean tokens | **2.0M** | **5.1M (~2.5×)** |

**Takeaway:** Under the same oracle standard and a one-rework cap on ad-hoc chat, BCC **completes the suite** with mostly first-try greens and **lower token cost**. Ad-hoc short-demand interaction does not reach final green within budget.

Row-level data: [scorecard.md](./scorecard.md). Task definitions: [tasks/](./tasks/).

## Why a control-plane skill wins here

1. **Plan-then-cut** focuses attention on one living brief and reduces partial implementations that fail edge-case oracles.  
2. **Global progress files** support multi-slice and recovery-style work without relying on chat memory alone.  
3. **Implement gates** keep coding aligned with the locked plan before large diffs.  
4. **Ad-hoc case-by-case prompting** optimizes for the next utterance, not for full-spec closure under a hard rework limit.

## PS — Role of “human” in the evaluation

In this evaluation, **human-in-the-loop decisions (including implement APPROVE) were enacted by agent subagents**, not by live human operators. Subagents followed a fixed policy (e.g. approve when the plan was locked and ready for clean-cut). Results measure the **skill workflow + automated gate policy**.
