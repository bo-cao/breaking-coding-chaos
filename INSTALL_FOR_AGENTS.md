# Install BCC (4 skills only)

Paste for your agent:

> Prefer the open Agent Skills CLI (no clone required):  
> `npx skills add jc/breaking-coding-chaos -g -y`  
> Installs exactly four BCC skills (`bcc-breaking-coding-chaos`, `bcc-throughline`, `bcc-plan-spar`, `bcc-clean-cut`) into detected agents (Claude Code, Codex, Cursor, OpenCode, Hermes, OpenClaw, …).  
> Pin agents: `npx skills add jc/breaking-coding-chaos -g -y -a claude-code -a codex -a cursor`.  
> Claude Code official plugin: `/plugin marketplace add jc/breaking-coding-chaos` then `/plugin install bcc@breaking-coding-chaos`.  
> From a local clone (Grok / offline): `.\install.ps1 -AllAgents` (Windows) or `./install.sh --all-agents` (Unix). Never leave `bcc` / `bcc-status` mini-skills. New session; verify only the four `bcc-*` names.

## One-liners

```bash
# All detected agents (global)
npx skills add jc/breaking-coding-chaos -g -y

# Claude Code only
npx skills add jc/breaking-coding-chaos -g -y -a claude-code

# Codex only
npx skills add jc/breaking-coding-chaos -g -y -a codex
```

Claude plugin (inside Claude Code):

```text
/plugin marketplace add jc/breaking-coding-chaos
/plugin install bcc@breaking-coding-chaos
```

## Invocable skills

| Slash | Role |
|-------|------|
| `/bcc-breaking-coding-chaos` | Main (Mode A or status) |
| `/bcc-throughline` | Global map |
| `/bcc-plan-spar` | PLAN align + review |
| `/bcc-clean-cut` | Minimal implement |

No separate `/bcc` or `/bcc-status` skills — status is built into the main skill.

Full matrix: [docs/install/README.md](./docs/install/README.md)
