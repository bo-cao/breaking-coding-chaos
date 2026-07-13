# Install BCC (4 skills only)

Paste for your agent:

> From the breaking-coding-chaos repo root, run `.\install.ps1 -AllAgents` (Windows) or `./install.sh --all-agents` (Unix) to install **exactly four** BCC skills into every supported agent (Grok, Claude, Cursor, Codex, agents, OpenCode `~/.config/opencode/skills`, Hermes `~/.hermes/skills`, OpenClaw `~/.openclaw/skills`). Default without flags is Grok-only. Never leave `bcc` / `bcc-status` mini-skills. New session; verify four names only: bcc-breaking-coding-chaos, bcc-throughline, bcc-plan-spar, bcc-clean-cut.

## Invocable skills

| Slash | Role |
|-------|------|
| `/bcc-breaking-coding-chaos` | Main (Mode A or status) |
| `/bcc-throughline` | Global map |
| `/bcc-plan-spar` | PLAN align + review |
| `/bcc-clean-cut` | Minimal implement |

No separate `/bcc` or `/bcc-status` skills — status is built into the main skill.
