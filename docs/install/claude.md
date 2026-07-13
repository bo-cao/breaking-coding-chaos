# Claude Code

Install **exactly four** skills:

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

## User skills (recommended)

macOS / Linux:

```bash
# from the breaking-coding-chaos repo root
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.claude/skills/
```

Windows (PowerShell):

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

Resulting layout:

```text
~/.claude/skills/
  bcc-breaking-coding-chaos/SKILL.md
  bcc-throughline/SKILL.md
  bcc-plan-spar/SKILL.md
  bcc-clean-cut/SKILL.md
```

## Project skills (repo-local)

Copy the same four folders into the project:

```bash
mkdir -p .claude/skills
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      .claude/skills/
```

Useful when the whole team should share BCC without touching user-global skills.

## After install

1. **Open a new Claude Code session** (or restart) so skills re-index.
2. Type `/` and confirm you see the four `bcc-*` skills.
3. Try:
   - `/bcc-throughline` — map / status
   - `/bcc-breaking-coding-chaos` — full Mode A chain
   - `/bcc-plan-spar` then `/bcc-clean-cut` — after throughline exists

## Optional: skills CLI (when repo is public)

```bash
npx skills add <you>/breaking-coding-chaos -y
```

## Uninstall

```bash
rm -rf ~/.claude/skills/bcc-breaking-coding-chaos \
       ~/.claude/skills/bcc-throughline \
       ~/.claude/skills/bcc-plan-spar \
       ~/.claude/skills/bcc-clean-cut
```

Windows:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\bcc-*"
```

## Notes

- Do **not** copy the whole `skills/*` tree if it ever gains non-BCC folders — name the four explicitly.
- Slash ids are `bcc-…`. Natural language that matches skill descriptions also works.
