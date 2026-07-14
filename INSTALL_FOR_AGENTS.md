# Install BCC (4 skills only)

Paste for your agent:

> Prefer the open Agent Skills CLI (no clone required):  
> `npx skills add bo-cao/breaking-coding-chaos -g -y`  
> Installs exactly four BCC skills (`bcc-breaking-coding-chaos`, `bcc-throughline`, `bcc-plan-spar`, `bcc-clean-cut`) into detected agents (Claude Code, Codex, Cursor, OpenCode, Hermes, OpenClaw, …).  
> Pin agents: `npx skills add bo-cao/breaking-coding-chaos -g -y -a claude-code -a codex -a cursor`.  
> Claude Code official plugin: `/plugin marketplace add bo-cao/breaking-coding-chaos` then `/plugin install bcc@breaking-coding-chaos`.  
> From a local clone (Grok / offline): `.\install.ps1 -AllAgents` (Windows) or `./install.sh --all-agents` (Unix). Never leave `bcc` / `bcc-status` mini-skills. New session; verify only the four `bcc-*` names.

## One-liners

```bash
# All detected agents (global)
npx skills add bo-cao/breaking-coding-chaos -g -y

# Claude Code only
npx skills add bo-cao/breaking-coding-chaos -g -y -a claude-code

# Codex only
npx skills add bo-cao/breaking-coding-chaos -g -y -a codex
```

Claude plugin (inside Claude Code):

```text
/plugin marketplace add bo-cao/breaking-coding-chaos
/plugin install bcc@breaking-coding-chaos
```

## Commands

Pipeline: throughline → plan-spar → **APPROVE** → clean-cut.  
**Mode A** (all-in-one): `/bcc-breaking-coding-chaos`. **Mode B** (step-by-step): start at `/bcc-throughline`.

| Slash | Args |
|-------|------|
| `/bcc-breaking-coding-chaos` | Mode A · `status` · optional `rounds=N` `review=…` |
| `/bcc-throughline` | Mode B entry · idea / rebalance |
| `/bcc-plan-spar` | **`rounds=N`** review cap (default `3`, `0`=skip) · `review=auto\|self\|subagent\|cli\|off` |
| `/bcc-clean-cut` | `lite` · `full` · `ultra` |

```text
# Mode A
/bcc-breaking-coding-chaos implement my idea
# Mode B
/bcc-throughline
/bcc-plan-spar HP1 rounds=3
/bcc-clean-cut
```

Full matrix: [docs/install/README.md](./docs/install/README.md) · [README.md](./README.md) · [简体中文](./READMEs/README.zh-CN.md) · [繁體中文](./READMEs/README.zh-TW.md)
