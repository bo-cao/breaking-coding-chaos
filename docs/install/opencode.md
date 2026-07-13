# OpenCode

OpenCode discovers Agent Skills (`SKILL.md`) from several roots ([docs](https://opencode.ai/docs/skills/)):

| Scope | Path |
|-------|------|
| **User (recommended)** | `~/.config/opencode/skills/<name>/SKILL.md` |
| Project | `.opencode/skills/<name>/SKILL.md` |
| Also scanned | `~/.claude/skills`, `~/.agents/skills` (compat) |

Windows: `%USERPROFILE%\.config\opencode\skills\` (and sometimes `%APPDATA%\opencode\skills\` via install script).

## Install BCC (4 skills only)

From the **breaking-coding-chaos** repo root:

```powershell
# User-global OpenCode (+ all other agents)
.\install.ps1 -AllAgents

# OpenCode only
.\install.ps1 -Dest "$env:USERPROFILE\.config\opencode\skills"
```

```bash
./install.sh --all-agents
# or
DEST="$HOME/.config/opencode/skills" ./install.sh
```

### Project-local (this repo / any workspace)

```powershell
.\install.ps1 -Project
# installs into .opencode/skills under cwd among others
```

```bash
./install.sh --project
```

Manual:

```bash
REPO=/path/to/breaking-coding-chaos
DEST="$HOME/.config/opencode/skills"
for s in bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut; do
  rm -rf "$DEST/$s"
  cp -R "$REPO/skills/$s" "$DEST/$s"
done
```

## Verify

Restart OpenCode or open a new session. You should see **exactly four** BCC skills:

- `/bcc-breaking-coding-chaos` — main (Mode A or status)
- `/bcc-throughline`
- `/bcc-plan-spar`
- `/bcc-clean-cut`

No `bcc` / `bcc-status` aliases.

## Invoke

Slash or natural language matching each skill’s short `description`.  
**Order:** throughline **before** plan-spar; human APPROVE before clean-cut.

## Uninstall

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.config\opencode\skills\bcc-*"
```

```bash
rm -rf ~/.config/opencode/skills/bcc-*
```
