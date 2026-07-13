# Install — breaking-coding-chaos

Install the **four** skill directories:

```text
skills/breaking-coding-chaos/
skills/throughline/
skills/plan-spar/
skills/clean-cut/
```

## Per agent

| Agent | Doc |
|-------|-----|
| Claude Code | [claude.md](./claude.md) |
| Codex | [codex.md](./codex.md) |
| Cursor | [cursor.md](./cursor.md) |
| Grok | [grok.md](./grok.md) |
| OpenCode | [opencode.md](./opencode.md) |
| Hermes | [hermes.md](./hermes.md) |
| OpenClaw | [openclaw.md](./openclaw.md) |

## Generic copy

```bash
REPO=/path/to/breaking-coding-chaos
DEST=<your-agent-skills-root>
cp -R "$REPO/skills/"* "$DEST/"
```

PowerShell:

```powershell
$Repo = "D:\path\to\breaking-coding-chaos"
$Dest = "$env:USERPROFILE\.grok\skills"
foreach ($s in "breaking-coding-chaos","throughline","plan-spar","clean-cut") {
  Copy-Item -Recurse -Force "$Repo\skills\$s" "$Dest\$s"
}
```

## Verify

- `/breaking-coding-chaos`
- `/throughline`
- `/plan-spar <slice>`
- `/clean-cut` (after APPROVE)
