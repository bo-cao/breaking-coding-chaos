# breaking-coding-chaos

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-4-informational)](./skills)
[![Agents](https://img.shields.io/badge/agents-Grok%20%7C%20Claude%20%7C%20Codex%20%7C%20Cursor%20%7C%20OpenCode%20%7C%20Hermes%20%7C%20OpenClaw-success)](./docs/install/README.md)

<p align="center">
  <img src="./assets/banner.jpg" alt="breaking-coding-chaos — dual-loop human-in-the-loop coding with agents" width="100%" />
</p>

**breaking-coding-chaos (BCC)** is a **human-in-the-loop dual-loop control-plane skill suite** for coding agents: you keep progress and technical detail under control while the agent ships your idea — without losing the plot.

**Works with all agents.** Standard Agent Skills layout (`SKILL.md` folders) — install once for Claude Code, Codex, Grok, Cursor, OpenCode, Hermes, OpenClaw, and any runtime that loads the same skill format.

[English](./README.md) | [简体中文](./READMEs/README.zh-CN.md) | [繁體中文](./READMEs/README.zh-TW.md)

> **Idea first.** Bring a **reasonably concrete idea** (what to build, what “done” means).  
> BCC helps you **implement it 1:1** with control over progress and technical detail — **not** invent a product from a blank void.  
> Without a real idea, there is nothing honest to code.

---

## Why a control plane

Agentic coding is powerful — and chronically **unreliable at the exact moment precision matters**.

When the work needs **fine-grained design**, **explicit trade-offs**, and **progress you can audit**, sessions often end in:

- **Memory collapse** — after `/clear`, compaction, or a long tool chain, goals and constraints evaporate. The agent rediscovers the same bugs and re-asks the same architecture questions.
- **Hallucinated certainty** — the model fills gaps with plausible inventiveness: wrong APIs, phantom modules, “fixes” that never touch the real failure mode.
- **Attention smear** — the more “helpful” global context you inject, the harder it becomes to put **all** of the model’s attention on the *one* hard problem in front of you.

### Long-term memory tools are not the same problem

There is a rich ecosystem of **agent memory** products and libraries — for example [mem0](https://github.com/mem0ai/mem0) and [agentmemory](https://github.com/rohitg00/agentmemory). They excel at **cross-session recall**, retrieval, and carrying identity/preferences through time.

That is valuable. It is also **a different shape of problem** from high-effort engineering:

| Global / fuzzy memory | High-effort implementation |
|-----------------------|----------------------------|
| “What did we decide last month?” | “What exactly do we code *this hour*, and how do we prove it?” |
| Soft retrieval over a large store | Hard contract: checklist + verification |
| More context can help chat | More context can **dilute** the critical path |
| Optimized for continuity | Optimized for **control** |

When the work is *hard* — a subtle concurrency bug, a paper-faithful experiment, a multi-module migration — a blurry global memory layer can become a **tax**: the agent half-remembers everything and fully owns nothing. You need a **control plane**: durable files for the *endeavor*, a *single* living coding brief for the *current hardpoint*, adversarial stress on that brief, then the **smallest correct diff**, with progress written back where you can see it.

That is **breaking-coding-chaos** (BCC).

---

## What the field already taught us (and what we compose)

We do **not** claim a single “main” endorsement. We **compose** several well-known, high-signal patterns into one dual-loop skill suite — openly, with credit.

| Pattern | What it taught the ecosystem | Where it lands in BCC |
|---------|------------------------------|------------------------|
| **Filesystem as context** (Manus-style *context engineering*) | Chat is RAM; disk is the real notebook | **bcc-throughline** |
| **Persistent file planning** ([planning-with-files](https://github.com/OthmanAdi/planning-with-files)) | Crash-proof markdown that survives `/clear` | Throughline mechanics |
| **Alignment + domain docs** ([Matt Pocock skills](https://github.com/mattpocock/skills)) | Shared language and ADRs before code | **bcc-plan-spar** |
| **Minimal diffs** ([ponytail](https://github.com/DietrichGebert/ponytail)) | YAGNI ladder; stop over-building | **bcc-clean-cut** |

**BCC’s contribution** is a **human-in-the-loop control plane**: dual loop, hard order (throughline → plan-spar → clean-cut), **one living `PLAN.md`**, forced writeback, and preflight so the wrong skill does not fire at the wrong time.

---

## How it works

<p align="center">
  <img src="./assets/architecture.png" alt="Ship your idea with agents — throughline progress, plan-spar one sub-task, clean-cut ships it" width="100%" />
</p>

<p align="center">
  <em>Dual loop. Human gates. One living plan per sub-task.</em>
</p>

### Dual loop in one sentence

**Throughline** sits on top: the **project progress bar** over whatever sub-tasks *you* mapped (A → B → C → D; not a fixed template).  
Under it, **plan-spar** and **clean-cut** cooperate on **one current sub-task** — lock a living `PLAN.md`, you APPROVE, minimal ship, write back; the bar moves, then the next sub-task gets the same pair again.

### Artifacts

| Layer | Files | Answers |
|-------|--------|---------|
| **Global (throughline only)** | `plans.md`, `progress.md`, `findings.md` | Where is the endeavor? What happened? What did we learn globally? |
| **Current coding** | **one** `PLAN.md` (rewrite per hardpoint) | What do we code *now*, and how do we verify? |
| **Support** | `CONTEXT.md`, `docs/adr/*` | Domain words; hard-to-reverse decisions |
| **Session (optional)** | `.bcc/session.json` | Cross-chat APPROVE + plan hash for clean-cut preflight |

### Pipeline by act

| Act | Skill | What happens | Artifacts | Example | **You** do |
|-----|--------|--------------|-----------|---------|------------|
| **0 · Map** | `bcc-throughline` | Goal, phases, hardpoint map; status & reprioritize | throughline trio | “4 RL teaching cases; ship 01–02 this week” | Approve / edit the map |
| **1 · Brief** | `bcc-plan-spar` | Human grill (≤10 turns, interrupt anytime); lock **single** `PLAN.md` | PLAN, CONTEXT, ADR | “Case 01: ε-greedy bandit, stdlib only” | Answer · **lock PLAN** |
| **2 · Stress** | `bcc-plan-spar` | Adversarial review (self / subagent / optional CLI); live log; revise PLAN | `PLAN-REVIEW-LOG.md` | Reviewer REVISE → add safety limits | **APPROVE implement** (or amend / stop) |
| **3 · Ship** | `bcc-clean-cut` | Minimal diff (YAGNI ladder) + verify + **mandatory writeback** | code + updated trio | `python train_eps.py` exits 0 | Escalate only if blocked |

**Details that matter:**

- Auto-review `VERDICT: APPROVED` **≠** permission to code — only your implement gate does.  
- `PLAN.md` is **not** sliced into many plan files; it is **updated in place**. History of the endeavor lives in **throughline**.  
- **plan-spar always after throughline** (hard preflight).  
- Clean-cut without writeback is **incomplete**.

### Four skills only

| Skill | Role |
|-------|------|
| **`bcc-breaking-coding-chaos`** | Main entry: Mode A chain **or** short status + next |
| **`bcc-throughline`** | Global cockpit |
| **`bcc-plan-spar`** | Align + review current PLAN |
| **`bcc-clean-cut`** | Minimal implement + writeback |

Slash ids use `bcc-…`. Chat may use `bcc:…` for readability (`argument-hint` on each skill).

### Two usage modes (short)

| | **Mode A — Agent chains** | **Mode B — You control** |
|--|---------------------------|---------------------------|
| Entry | `/bcc-breaking-coding-chaos` | `/bcc-throughline` (or any sub-skill) |
| Order | Thin orchestrator loads children in sequence | You invoke each step |
| Best for | First use, large goals | Status checks, precise control |

Same four skills, same files. Mixing is fine.

---

## Worked example: multi-slice + HITL

Plan **four** cases; ship **two** this session.

```text
bcc-throughline          →  map 01–04; this session ships 01+02 only
bcc-plan-spar 01         →  lock PLAN → review → YOU approve implement
bcc-clean-cut 01         →  code + verify → writeback
bcc-plan-spar 02         →  lock PLAN → review (may REVISE) → YOU approve
bcc-clean-cut 02         →  code + verify → writeback
bcc-throughline          →  01/02 complete; 03/04 still pending
```

| # | Stage | Gate | Your decision (example) |
|---|--------|------|-------------------------|
| 0 | throughline | Map scope | Approve 4-case map; ship **01+02** only |
| 1 | plan-spar 01 | Lock PLAN | **LOCK PLAN NOW** |
| 2 | plan-spar 01 | Implement | **APPROVE IMPLEMENT** → clean-cut |
| 3 | plan-spar 02 | Lock PLAN | **LOCK PLAN NOW** |
| 4 | plan-spar 02 review | Agent REVISE | *(not HITL)* builder updates PLAN |
| 5 | plan-spar 02 | Implement | **APPROVE IMPLEMENT** → clean-cut |

| Who | Typical actions |
|-----|-----------------|
| **You** | Map · lock PLAN · implement gate · reprioritize |
| **Agent** | Grill · artifacts · review · cut after APPROVE · writeback |

---

## Who it’s for

| Identity | Why BCC helps |
|----------|----------------|
| **Engineers / tech leads** shipping production or multi-module work | Keep design trade-offs and “what’s done” visible across long agent sessions |
| **Indie builders & founders** coding with agents | Ship an idea step by step without the agent rewriting the whole product every chat |
| **Researchers & advanced students** (methods, experiments, paper-faithful code) | Hard constraints and verification stay in files, not in fuzzy chat memory |
| **Maintainers of large / greenfield repos** | Global map + one hard slice at a time; less thrash after `/clear` or context loss |
| **Anyone who already uses Claude / Codex / Cursor / …** | Same four skills on every agent — one workflow, many runtimes |

## When to use it

| Scenario | Fit |
|----------|-----|
| Multi-step or multi-week endeavor with several natural sub-tasks | **Strong** — throughline owns the bar; plan-spar/clean-cut per slice |
| High-stakes slice: subtle bug, migration, experiment that must match a brief | **Strong** — lock PLAN, stress-test, you APPROVE, then minimal ship |
| Resume after `/clear`, compaction, or switching agents | **Strong** — progress lives in files on disk |
| “Vibe” one-liners or throwaway scripts | **Weak** — overkill; just chat |
| No concrete idea yet (only “build me something cool”) | **Wrong tool** — BCC implements ideas; it does not invent products |

---

## Quick start

Exactly **four** skills (no more):

`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`

Primary guides: **Claude Code** and **Codex**. Other agents are secondary below.

---

### Claude Code (primary)

**1. User skills** (global, recommended):

```bash
# from this repo root — macOS / Linux
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.claude/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

**2. Or project skills** (team / repo-local):

```bash
mkdir -p .claude/skills
cp -R skills/bcc-breaking-coding-chaos skills/bcc-throughline \
      skills/bcc-plan-spar skills/bcc-clean-cut .claude/skills/
```

| Scope | Path |
|-------|------|
| User | `~/.claude/skills/<name>/SKILL.md` |
| Project | `.claude/skills/<name>/SKILL.md` |

**3. Use it**

1. Open a **new** Claude Code session (skills re-index on start).
2. Type `/` — confirm the four `bcc-*` entries.
3. Try `/bcc-throughline` or `/bcc-breaking-coding-chaos`.

Full guide: [docs/install/claude.md](./docs/install/claude.md).  
When the repo is public: `npx skills add <you>/breaking-coding-chaos -y`.

---

### Codex (primary)

Codex is **opt-in** (keeps the global skills list lean).

**1. Install to Codex skills** (and optionally the shared agents path):

```bash
# from this repo root — macOS / Linux
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.codex/skills/

# many Codex setups also read:
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.agents/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

| Path | Role |
|------|------|
| `~/.codex/skills/` | Codex primary skills root |
| `~/.agents/skills/` | Shared agents skill root (often also scanned) |

**2. Use it**

1. **Restart Codex** or open a **new thread**.
2. Open the skills list — you should see **only these four** BCC folders (no mini-routers).
3. Invoke from the skills UI, or with natural language that matches each skill description.

Full guide: [docs/install/codex.md](./docs/install/codex.md).

---

### Everyone else (secondary)

One-shot install for all supported agents:

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

| Agent | Skills root | Guide |
|-------|-------------|--------|
| Grok | `~/.grok/skills/` | [grok.md](./docs/install/grok.md) · default of `install.ps1` |
| Cursor | `~/.cursor/skills/` | [cursor.md](./docs/install/cursor.md) |
| OpenCode | `~/.config/opencode/skills/` | [opencode.md](./docs/install/opencode.md) |
| Hermes | `~/.hermes/skills/` | [hermes.md](./docs/install/hermes.md) |
| OpenClaw | `~/.openclaw/skills/` | [openclaw.md](./docs/install/openclaw.md) |

Paste block: [INSTALL_FOR_AGENTS.md](./INSTALL_FOR_AGENTS.md) · full matrix: [docs/install/README.md](./docs/install/README.md)

**Verify (any agent):** new session → list skills → only the four `bcc-*` names above.

---

## Artifacts

| File | Owner |
|------|--------|
| `plans.md` `progress.md` `findings.md` | bcc-throughline |
| `CONTEXT.md` `docs/adr/*` | bcc-plan-spar |
| `PLAN.md` (single, living) | plan-spar + clean-cut |
| `.bcc/session.json` | APPROVE / preflight (optional) |

---

## Acknowledgments

BCC re-encapsulates ideas under our own skill names. We are **not** affiliated with the projects below — thank you to these authors and communities.

- [planning-with-files — Manus-style persistent markdown planning (throughline inspiration)](https://github.com/OthmanAdi/planning-with-files)
- [Manus context engineering — filesystem as durable agent context](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Matt Pocock skills — grill / grill-with-docs and domain modeling (plan-spar inspiration)](https://github.com/mattpocock/skills)
- [ponytail — YAGNI / minimal implementation ladder (clean-cut inspiration)](https://github.com/DietrichGebert/ponytail)

Further design notes: [DIRECTION.md](./DIRECTION.md).

---

## Benchmarks

Placeholder — representative tasks and scorecards will land under `benchmark/`.

---

## Star History

<p align="center">
  <sub>SIGNAL</sub><br />
  <strong>Leave a star if BCC helped you ship</strong><br />
  <sub>Not a vanity metric — a breadcrumb for the next person who needs a control plane.</sub>
</p>

<p align="center">
  <img src="./assets/star-history.svg" alt="Star trajectory (illustrative until the repo is public)" width="100%" />
</p>

<p align="center">
  <sub>This curve is a <strong>static illustration</strong> in the repo — not live GitHub data. After you publish, stars are recorded by GitHub; use the links below for real numbers.</sub>
</p>

<p align="center">
  <a href="https://github.com/OWNER/breaking-coding-chaos"><strong>★&nbsp; Star this repo</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/OWNER/breaking-coding-chaos/stargazers">Stargazers</a>
  &nbsp;·&nbsp;
  <a href="https://www.star-history.com/#OWNER/breaking-coding-chaos&Date">Live curve</a>
</p>

<p align="center">
  <sub>Replace <code>OWNER</code> when public.</sub>
</p>

---

## License

MIT — see [LICENSE](./LICENSE).

Copyright (c) 2026 breaking-coding-chaos contributors (anonymous for now; may be updated to a GitHub username later).
