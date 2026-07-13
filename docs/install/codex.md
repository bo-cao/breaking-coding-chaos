# Codex

Install **exactly four** skills:

- `bcc-breaking-coding-chaos`
- `bcc-throughline`
- `bcc-plan-spar`
- `bcc-clean-cut`

BCC is **not** installed to Codex by default (keeps the global skills list lean). Install only when you want it.

## User skills

macOS / Linux:

```bash
# from the breaking-coding-chaos repo root
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.codex/skills/

# Many Codex / agent setups also read the shared agents path:
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.agents/skills/
```

Windows (PowerShell):

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

Resulting layout:

```text
~/.codex/skills/
  bcc-breaking-coding-chaos/SKILL.md
  bcc-throughline/SKILL.md
  bcc-plan-spar/SKILL.md
  bcc-clean-cut/SKILL.md
```

## After install

1. **Restart Codex** or open a **new thread** so skills re-index.
2. Open the skills UI / list — you should see **only these four** BCC entries (no mini-routers or alias folders).
3. Invoke from the skills menu, or with natural language that matches each skill description, for example:
   - “run throughline” / map progress
   - “plan-spar this slice”
   - “clean-cut implement PLAN”

## Optional: install everything at once

If you also use Claude, Cursor, Grok, etc.:

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

This includes Codex + `~/.agents/skills`.

## Uninstall

```bash
rm -rf ~/.codex/skills/bcc-* ~/.agents/skills/bcc-*
```

Windows:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\bcc-*"
Remove-Item -Recurse -Force "$env:USERPROFILE\.agents\skills\bcc-*" -ErrorAction SilentlyContinue
```

## Notes

- Four folders max — no `bcc` / `bcc-status` aliases.
- Prefer explicit copy of the four names over `cp -R skills/*` if the repo layout ever grows.
