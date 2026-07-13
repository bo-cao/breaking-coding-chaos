# breaking-coding-chaos

**Human-in-the-loop skill suite for shipping real work with coding agents — without losing the plot.**

[English](./README.md) | [简体中文](./READMEs/README.zh-CN.md) | [繁體中文](./READMEs/README.zh-TW.md)

If you have a **reasonable idea**, ship it **step by step**:

1. **throughline** — see progress and adjust the whole endeavor  
2. **plan-spar** — align a slice, lock/trim `PLAN.md`, spar it, you APPROVE  
3. **clean-cut** — implement that PLAN with a **minimal diff** (ponytail ladder), verify, write back  

Works with Agent Skills hosts: Claude · Codex · Cursor · Grok · OpenCode · Hermes · OpenClaw

---

## Why

- Progress dies in chat after `/clear`  
- Idea and code diverge; no verification loop  
- Agents over-build  
- You cannot see or steer *where the endeavor is*

---

## Skills (four)

| Skill | Job | Inspired by (mechanism) |
|-------|-----|-------------------------|
| **`breaking-coding-chaos`** | Orchestrator | — |
| **`throughline`** | Progress visibility + adjustment | planning-with-files |
| **`plan-spar`** | Align → lock/update/约减 PLAN → spar → your APPROVE | grill-with-docs + domain-modeling |
| **`clean-cut`** | **Write code** from PLAN: YAGNI ladder + verify | **ponytail** (coding only) |

```text
throughline              plan-spar                    clean-cut
─────────────            ─────────                    ─────────
plans.md                 CONTEXT · ADR · PLAN.md      min code
progress.md              lock → spar ⇄ you            verify
findings.md              (no product code)            约减 PLAN
"Where are we?"                   │                        │
     ▲                            └── APPROVE ─────────────┘
     └──────────────── writeback after clean-cut ──────────┘
```

**Naming:**

- **plan-spar** = work on the *plan* (align + spar)  
- **clean-cut** = *cut* the code clean (ponytail) — not buried inside plan-spar  

---

## Example usage

### Example A — Full suite

**You:** `/breaking-coding-chaos` — CLI Markdown → Anki; cloze parsing first.

**Agent (throughline):** creates `plans.md` / `progress.md` / `findings.md`; you tweak phases.

**You:** first slice = cloze only.

**Agent (`plan-spar`):** questions → `CONTEXT.md` → **locks `PLAN.md`** → spars plan → asks **APPROVE**.

**You:** APPROVE.

**Agent (`clean-cut`):** minimal implementation + verify against PLAN → trim PLAN → writeback throughline.

**You:** `/throughline` — where are we? move CLI polish after tests.

**You:** `/plan-spar` next slice → APPROVE → `/clean-cut` (or agent continues suite handoff).

### Example B — Chat triggers

| You say | Skill |
|---------|--------|
| “Where are we? Drop phase 3.” | `throughline` |
| “plan-spar: payment webhook” | `plan-spar` |
| “APPROVE / implement the PLAN / clean-cut” | `clean-cut` |
| “Run BCC on my prototype” | `breaking-coding-chaos` |

### Example C — PLAN lifecycle

| Step | Who | `PLAN.md` |
|------|-----|-----------|
| New slice | plan-spar | **Lock** |
| Spar / amend | plan-spar | **Update / 约减** |
| Implement | clean-cut | Execute + complete items + **约减** |
| Slice done | clean-cut + throughline | Story → `progress.md` |

---

## Install

Copy all four folders under `skills/` into your agent skills root:

`breaking-coding-chaos` · `throughline` · `plan-spar` · `clean-cut`

See [docs/install/README.md](./docs/install/README.md).

```bash
git clone https://github.com/<you>/breaking-coding-chaos.git
cp -r breaking-coding-chaos/skills/* ~/.grok/skills/   # example
```

---

## Artifacts

| File | Primary owner |
|------|----------------|
| `plans.md` `progress.md` `findings.md` | throughline |
| `CONTEXT.md` `docs/adr/*` | plan-spar |
| `PLAN.md` | plan-spar (contract) + clean-cut (execute/trim) |

---

## Benchmarks

Placeholder — `benchmark/` later.

---

## Inspired by

| Our skill | Upstream ideas |
|-----------|----------------|
| `throughline` | [planning-with-files](https://github.com/OthmanAdi/planning-with-files) |
| `plan-spar` | [grill-with-docs / domain-modeling](https://github.com/mattpocock/skills) |
| `clean-cut` | [ponytail](https://github.com/DietrichGebert/ponytail) coding ladder |

We re-encapsulate under our names. See `DIRECTION.md` §0a. Not affiliated.

---

## Repo layout

```text
skills/
  breaking-coding-chaos/
  throughline/
  plan-spar/
  clean-cut/          # ← ponytail lives here
docs/install/
READMEs/
DIRECTION.md
```

---

## License

MIT — [LICENSE](./LICENSE).
