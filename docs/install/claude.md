# Claude Code

Install **exactly four** skills:

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

## Recommended — official plugin marketplace

In **Claude Code** (interactive):

```text
/plugin marketplace add jc/breaking-coding-chaos
/plugin install bcc@breaking-coding-chaos
```

Or non-interactive CLI:

```bash
claude plugin marketplace add jc/breaking-coding-chaos
claude plugin install bcc@breaking-coding-chaos
```

This is Claude’s first-party plugin flow ([plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)). Skills ship from this repo’s `skills/` tree via [`.claude-plugin/marketplace.json`](../../.claude-plugin/marketplace.json).

Then open a **new** session, type `/`, and confirm the four `bcc-*` skills.

## Alternative — Agent Skills CLI (one line)

Same open standard used across agents ([vercel-labs/skills](https://github.com/vercel-labs/skills)):

```bash
npx skills add jc/breaking-coding-chaos -g -y -a claude-code
```

Global path: `~/.claude/skills/<name>/SKILL.md`.

Project-scoped (share with the team via git):

```bash
# from your product repo (not necessarily this one)
npx skills add jc/breaking-coding-chaos -y -a claude-code
```

## From a local clone

```bash
# macOS / Linux — repo root
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.claude/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

## After install

1. **New Claude Code session** (skills re-index on start).  
2. Type `/` — confirm four `bcc-*` entries.  
3. Try:
   - `/bcc-throughline` — map / status  
   - `/bcc-breaking-coding-chaos` — full Mode A chain  
   - `/bcc-plan-spar` then `/bcc-clean-cut` — after throughline exists  

## Uninstall

Plugin:

```text
/plugin uninstall bcc@breaking-coding-chaos
```

Skills CLI:

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a claude-code -y
```

Manual:

```bash
rm -rf ~/.claude/skills/bcc-*
```

## Notes

- Prefer **plugin** or **`npx skills add`** over hand-copying when possible.  
- Slash ids are `bcc-…`. Natural language that matches skill descriptions also works.  
- Do not invent extra mini-skills (`bcc`, `bcc-status`).
