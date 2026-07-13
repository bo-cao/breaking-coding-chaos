# Grok

**User:** `~/.grok/skills/<name>/`  
**Project:** `<repo>/.grok/skills/<name>/`

```powershell
$Repo = "D:\path\to\breaking-coding-chaos"
$Dest = "$env:USERPROFILE\.grok\skills"
foreach ($s in "breaking-coding-chaos","throughline","plan-spar","clean-cut") {
  Copy-Item -Recurse -Force "$Repo\skills\$s" "$Dest\$s"
}
```

Skills auto-reload when files change. Invoke `/breaking-coding-chaos`, `/throughline`, `/plan-spar`, `/clean-cut`.
