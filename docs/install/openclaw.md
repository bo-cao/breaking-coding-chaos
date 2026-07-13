# OpenClaw

Global: `~/.openclaw/skills/`  
Project / workspace-style: `skills/` under the workspace  
([OpenClaw skills docs](https://docs.openclaw.ai/tools/skills))

## Recommended — Agent Skills CLI

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a openclaw
```

## From a local clone

```bash
DEST="$HOME/.openclaw/skills" ./install.sh
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.openclaw\skills"
```

Or:

```bash
./install.sh --all-agents
./install.sh --project   # also writes ./skills among others
```

## After install

New session; confirm four `bcc-*` skills.

## Uninstall

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a openclaw -y
```
