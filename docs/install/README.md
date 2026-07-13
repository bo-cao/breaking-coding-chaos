# Install — breaking-coding-chaos

## Fast path

From repo root — **4 skills only**:

```powershell
.\install.ps1                 # default: ~/.grok/skills
.\install.ps1 -AllAgents      # Grok + Claude + Cursor + Codex + agents
                              # + OpenCode + Hermes + OpenClaw
.\install.ps1 -Project        # project .grok / .claude / .cursor / .agents / .opencode / skills
```

```bash
./install.sh
./install.sh --all-agents
./install.sh --project
```

Paste-for-agents: [INSTALL_FOR_AGENTS.md](../../INSTALL_FOR_AGENTS.md)

## What gets installed

```text
bcc-breaking-coding-chaos/   # main (+ nested references/)
bcc-throughline/
bcc-plan-spar/
bcc-clean-cut/
```

Obsolete (`bcc`, `bcc-status`, loose SESSION/WRITEBACK at skills root) are **removed** on install.

## Agent paths (user-global)

| Agent | Skills directory |
|-------|------------------|
| **Grok** | `~/.grok/skills/` |
| **Claude Code** | `~/.claude/skills/` |
| **Cursor** | `~/.cursor/skills/` |
| **Codex / agents** | `~/.codex/skills/`, `~/.agents/skills/` |
| **OpenCode** | `~/.config/opencode/skills/` ([docs](https://opencode.ai/docs/skills/)) |
| **Hermes** | `~/.hermes/skills/` ([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)) |
| **OpenClaw** | `~/.openclaw/skills/` (+ workspace `skills/`) |

## Per-agent guides

**Primary (detailed):** Claude Code · Codex  

| Agent | Doc |
|-------|-----|
| **Claude Code** | [claude.md](./claude.md) |
| **Codex** | [codex.md](./codex.md) |
| Grok | [grok.md](./grok.md) |
| Cursor | [cursor.md](./cursor.md) |
| OpenCode | [opencode.md](./opencode.md) |
| Hermes | [hermes.md](./hermes.md) |
| OpenClaw | [openclaw.md](./openclaw.md) |

## Verify (any agent)

After install + new session, invocable BCC skills should be **exactly four**:

1. `bcc-breaking-coding-chaos`
2. `bcc-throughline`
3. `bcc-plan-spar`
4. `bcc-clean-cut`

## Manual one-liner pattern

```bash
REPO=/path/to/breaking-coding-chaos
DEST=<agent-skills-root>
for s in bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut; do
  rm -rf "$DEST/$s" && cp -R "$REPO/skills/$s" "$DEST/$s"
done
```
