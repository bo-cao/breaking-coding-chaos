# Cursor

Install **exactly four** skills into Cursor’s Agent Skills roots  
([Cursor skills docs](https://cursor.com/docs/context/skills)):

- **Global:** `~/.cursor/skills/<name>/`  
- **Project:** often `.agents/skills/` or `.cursor/skills/` (depending on tool)

## Recommended — Agent Skills CLI

```bash
npx skills add jc/breaking-coding-chaos -g -y -a cursor
```

Project-scoped (commit with the repo for the team):

```bash
npx skills add jc/breaking-coding-chaos -y -a cursor
```

## From a local clone

```bash
mkdir -p ~/.cursor/skills
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.cursor/skills/
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.cursor\skills"
```

## After install

Reload the Cursor window if skills do not appear. Invoke via slash skills or chat triggers in each skill’s `description`.

## Uninstall

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a cursor -y
```
