# Codex

Install **exactly four** skills:

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

BCC is **opt-in** for Codex (keeps the global skills list lean).

## Recommended — Agent Skills CLI (official multi-agent path)

Codex loads skills from `~/.codex/skills/` ([Codex skills docs](https://developers.openai.com/codex/skills)). The open skills CLI installs there with `-a codex`:

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a codex
```

Optional: also install the shared agents path some setups scan:

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a codex -a amp
# amp / universal-style agents often use ~/.agents/skills or ~/.config/agents/skills
```

List first:

```bash
npx skills add bo-cao/breaking-coding-chaos --list
```

## From a local clone

```bash
# macOS / Linux — repo root
mkdir -p ~/.codex/skills ~/.agents/skills
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.codex/skills/
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.agents/skills/
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

Layout:

```text
~/.codex/skills/
  bcc-breaking-coding-chaos/SKILL.md
  bcc-throughline/SKILL.md
  bcc-plan-spar/SKILL.md
  bcc-clean-cut/SKILL.md
```

## After install

1. **Restart Codex** or open a **new thread**.  
2. Skills UI / list — only these four BCC entries.  
3. Invoke from the skills menu or natural language (“run throughline”, “plan-spar this slice”, “clean-cut implement PLAN”).

## Uninstall

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a codex -y
# or
rm -rf ~/.codex/skills/bcc-* ~/.agents/skills/bcc-*
```

## Notes

- Prefer `npx skills add … -a codex` over manual copy.  
- Four folders max — no `bcc` / `bcc-status` aliases.
