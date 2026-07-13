# Hermes Agent

Hermes treats **`~/.hermes/skills/`** as the source of truth for skills ([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)).

Each skill is a directory containing `SKILL.md` (optionally nested under categories; BCC installs **flat** at the skills root for simplicity).

| Scope | Path |
|-------|------|
| **User (primary)** | `~/.hermes/skills/<name>/SKILL.md` |
| Optional | `skills.external_dirs` in Hermes `config.yaml` (point at a shared copy) |

Windows: `%USERPROFILE%\.hermes\skills\`

## Install BCC (4 skills only)

```powershell
.\install.ps1 -AllAgents
# Hermes only:
.\install.ps1 -Dest "$env:USERPROFILE\.hermes\skills"
```

```bash
./install.sh --all-agents
DEST="$HOME/.hermes/skills" ./install.sh
```

Manual:

```bash
REPO=/path/to/breaking-coding-chaos
DEST="$HOME/.hermes/skills"
for s in bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut; do
  rm -rf "$DEST/$s"
  cp -R "$REPO/skills/$s" "$DEST/$s"
done
```

### Optional: external_dirs (team share)

In `~/.hermes/config.yaml` (schema may vary by version):

```yaml
skills:
  external_dirs:
    - /path/to/breaking-coding-chaos/skills
```

Prefer a **copy** via install script so local edits and Hub skills do not fight over the same tree.

## Verify

```bash
hermes skills list
# or inside session:
/skills
```

Expect these four names (and no `bcc` / `bcc-status`):

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

New session after install. Invoke with `/skill <name>` or natural language.

## Workflow reminder

1. Idea must be reasonably concrete (1:1 implement).  
2. **throughline** first → then **plan-spar** → APPROVE → **clean-cut**.  
3. Main skill can chain Mode A or answer status.

## Uninstall

```bash
rm -rf ~/.hermes/skills/bcc-breaking-coding-chaos \
       ~/.hermes/skills/bcc-throughline \
       ~/.hermes/skills/bcc-plan-spar \
       ~/.hermes/skills/bcc-clean-cut
```
