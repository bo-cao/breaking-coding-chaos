# OpenCode

Global skills root: `~/.config/opencode/skills/`  
([OpenCode skills docs](https://opencode.ai/docs/skills/))

## Recommended — Agent Skills CLI

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a opencode
```

## From a local clone

```bash
DEST="$HOME/.config/opencode/skills" ./install.sh
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.config\opencode\skills"
# Windows sometimes also uses:
.\install.ps1 -Dest "$env:APPDATA\opencode\skills"
```

Or install every agent path:

```bash
./install.sh --all-agents
```

## Project-local

```bash
npx skills add bo-cao/breaking-coding-chaos -y -a opencode
# or
./install.sh --project
```

## After install

New OpenCode session; confirm four `bcc-*` skills.

## Uninstall

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a opencode -y
```
