# Hermes

Global skills root: `~/.hermes/skills/`  
([Hermes skills docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills))

Each skill is a directory with `SKILL.md` (BCC installs **flat** at the skills root).

## Recommended — Agent Skills CLI

```bash
npx skills add jc/breaking-coding-chaos -g -y -a hermes-agent
```

## From a local clone

```bash
DEST="$HOME/.hermes/skills" ./install.sh
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.hermes\skills"
```

Or:

```bash
./install.sh --all-agents
```

Prefer a **copy** (install script / CLI) so local edits and Hub skills do not fight over the same tree.

## After install

New session. Invoke with `/skill <name>` or natural language. Expect four `bcc-*` skills.

## Uninstall

```bash
npx skills remove bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut -g -a hermes-agent -y
# or
rm -rf ~/.hermes/skills/bcc-*
```
