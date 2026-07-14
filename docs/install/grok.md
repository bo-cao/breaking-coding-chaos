# Grok

Grok reads skills from `~/.grok/skills/`. Prefer the **clone install scripts** (or copy) — the open skills CLI may not detect Grok as a target agent.

## Recommended — install script

```powershell
# Windows — from this repo root
.\install.ps1
```

```bash
# macOS / Linux
./install.sh
```

Installs **exactly four** folders under `~/.grok/skills/`.

## Manual copy

```bash
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.grok/skills/
```

## Multi-agent on this machine

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

Also consider the open CLI for Claude/Codex/Cursor/etc.:

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y
```

## After install

New Grok session:

```text
/bcc-throughline
/bcc-plan-spar … rounds=3
/bcc-clean-cut
/bcc-breaking-coding-chaos status
```

See [README.md](../../README.md).
