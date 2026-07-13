# OpenClaw

OpenClaw loads Agent Skills from managed and workspace paths:

| Scope | Path |
|-------|------|
| **User / managed** | `~/.openclaw/skills/<name>/SKILL.md` |
| Workspace | `<workspace>/skills/<name>/SKILL.md` |
| Compat | `~/.agents/skills/` (often also scanned) |

Windows: `%USERPROFILE%\.openclaw\skills\`

## Install BCC (4 skills only)

### User-global

```powershell
.\install.ps1 -AllAgents
# OpenClaw only:
.\install.ps1 -Dest "$env:USERPROFILE\.openclaw\skills"
```

```bash
./install.sh --all-agents
DEST="$HOME/.openclaw/skills" ./install.sh
```

### Workspace (OpenClaw employee / project folder)

```powershell
.\install.ps1 -Project
# copies into .\skills\ under cwd (OpenClaw workspace style) among others
```

```bash
./install.sh --project
# or manual into a specific workspace:
REPO=/path/to/breaking-coding-chaos
WS=/path/to/openclaw-workspace
for s in bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut; do
  rm -rf "$WS/skills/$s"
  mkdir -p "$WS/skills"
  cp -R "$REPO/skills/$s" "$WS/skills/$s"
done
```

Manual user install:

```bash
REPO=/path/to/breaking-coding-chaos
DEST="$HOME/.openclaw/skills"
for s in bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut; do
  rm -rf "$DEST/$s"
  cp -R "$REPO/skills/$s" "$DEST/$s"
done
```

## Verify

Restart OpenClaw gateway / new session. List skills (UI or docs command for your build). You should see **exactly four** BCC folders:

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

No separate `bcc` / `bcc-status` skills.

## Invoke

Skill entry or natural language matching each skill’s `description`.  
Hard order: **throughline → plan-spar → (APPROVE) → clean-cut**.

## Uninstall

```bash
rm -rf ~/.openclaw/skills/bcc-*
# workspace:
rm -rf /path/to/workspace/skills/bcc-*
```
