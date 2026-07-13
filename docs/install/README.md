# Install — breaking-coding-chaos

Exactly **four** skills:  
`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`

## One-line install (recommended)

Uses the open [Agent Skills](https://agentskills.io) CLI ([vercel-labs/skills](https://github.com/vercel-labs/skills)) — works with Claude Code, Codex, Cursor, OpenCode, Hermes, OpenClaw, and many more:

```bash
# Global install for every detected agent
npx skills add bo-cao/breaking-coding-chaos -g -y
```

```bash
# Or only the agents you use
npx skills add bo-cao/breaking-coding-chaos -g -y \
  -a claude-code -a codex -a cursor -a opencode -a hermes-agent -a openclaw
```

```bash
# List skills in this repo without installing
npx skills add bo-cao/breaking-coding-chaos --list
```

Then **start a new session** in each agent and confirm the four `bcc-*` names.

| Scope | Flag | Where skills land |
|-------|------|-------------------|
| **Global** (recommended) | `-g` | Per-agent user dir (e.g. `~/.claude/skills/`) |
| **Project** | (default, omit `-g`) | `./.claude/skills/`, `./.agents/skills/`, … under the current repo |

Official CLI reference: [skills.sh](https://skills.sh) · [vercel-labs/skills](https://github.com/vercel-labs/skills)

## Official per-agent shortcuts

| Agent | Preferred install | Details |
|-------|-------------------|---------|
| **Claude Code** | `/plugin marketplace add bo-cao/breaking-coding-chaos` then `/plugin install bcc@breaking-coding-chaos` · or `npx skills add … -a claude-code -g -y` | [claude.md](./claude.md) |
| **Codex** | `npx skills add bo-cao/breaking-coding-chaos -g -y -a codex` | [codex.md](./codex.md) |
| **Cursor** | `npx skills add bo-cao/breaking-coding-chaos -g -y -a cursor` | [cursor.md](./cursor.md) |
| **Grok** | Clone + `.\install.ps1` / `./install.sh` → `~/.grok/skills/` | [grok.md](./grok.md) |
| **OpenCode** | `npx skills add … -a opencode -g -y` | [opencode.md](./opencode.md) |
| **Hermes** | `npx skills add … -a hermes-agent -g -y` | [hermes.md](./hermes.md) |
| **OpenClaw** | `npx skills add … -a openclaw -g -y` | [openclaw.md](./openclaw.md) |

## From a local clone (offline / Grok / custom path)

```powershell
.\install.ps1                 # default: ~/.grok/skills
.\install.ps1 -AllAgents      # every known agent path on this machine
.\install.ps1 -Project        # project-local skill dirs under cwd
.\install.ps1 -Dest PATH      # one custom skills root
```

```bash
./install.sh
./install.sh --all-agents
./install.sh --project
DEST=~/.claude/skills ./install.sh
```

## What gets installed

```text
bcc-breaking-coding-chaos/   # main (+ nested references/)
bcc-throughline/
bcc-plan-spar/
bcc-clean-cut/
```

Obsolete mini-skills (`bcc`, `bcc-status`, loose SESSION/WRITEBACK at skills root) are **removed** by the clone install scripts.

## Agent paths (user-global)

| Agent | Skills directory (global) |
|-------|---------------------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` (also often `~/.agents/skills/`) |
| Cursor | `~/.cursor/skills/` |
| Grok | `~/.grok/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Hermes | `~/.hermes/skills/` |
| OpenClaw | `~/.openclaw/skills/` |

## Verify (any agent)

After install + **new session**, invocable BCC skills should be **exactly four**:

1. `bcc-breaking-coding-chaos`
2. `bcc-throughline`
3. `bcc-plan-spar`
4. `bcc-clean-cut`

## Update / remove (skills CLI)

```bash
npx skills update -g
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -y
```

Paste block for agents: [INSTALL_FOR_AGENTS.md](../../INSTALL_FOR_AGENTS.md)
