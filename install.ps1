# Install BCC: exactly 4 skills (1 main + 3 subs).
# Usage:
#   .\install.ps1                 # Grok only (default)
#   .\install.ps1 -AllAgents      # Grok + Claude + Cursor + Codex + agents + OpenCode + Hermes + OpenClaw
#   .\install.ps1 -Project        # project-local skill dirs under cwd
#   .\install.ps1 -Dest PATH

param(
  [string]$Dest = "",
  [switch]$AllAgents,
  [switch]$Project
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSrc = Join-Path $Root "skills"

$names = @(
  "bcc-breaking-coding-chaos",
  "bcc-throughline",
  "bcc-plan-spar",
  "bcc-clean-cut"
)

function Install-To([string]$targetRoot) {
  if (-not $targetRoot) { return }
  if (-not (Test-Path $targetRoot)) {
    New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
  }
  Get-ChildItem $targetRoot -Force -ErrorAction SilentlyContinue |
    Where-Object {
      $_.Name -in @("bcc", "bcc-status") -or
      $_.Name -in @("BCC-SESSION.md", "BCC-WRITEBACK.md", "SESSION.md", "WRITEBACK.md")
    } | ForEach-Object {
      Remove-Item -Recurse -Force $_.FullName
      Write-Host "  - removed obsolete $($_.Name)"
    }
  foreach ($n in $names) {
    $src = Join-Path $SkillsSrc $n
    if (-not (Test-Path $src)) {
      Write-Warning "Missing: $src"
      continue
    }
    $dst = Join-Path $targetRoot $n
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    Copy-Item -Recurse -Force $src $dst
    Write-Host "  + $n"
  }
}

function Test-AgentHome([string]$path) {
  if (-not $path) { return $false }
  if (Test-Path $path) { return $true }
  $parent = Split-Path $path -Parent
  return (Test-Path $parent)
}

Write-Host "BCC install (4 skills only). Source: $SkillsSrc"

if ($Dest) {
  Write-Host "-> $Dest"
  Install-To $Dest
}
elseif ($AllAgents) {
  $userHome = $env:USERPROFILE
  $list = @(
    (Join-Path $userHome ".grok\skills"),
    (Join-Path $userHome ".claude\skills"),
    (Join-Path $userHome ".cursor\skills"),
    (Join-Path $userHome ".agents\skills"),
    (Join-Path $userHome ".codex\skills"),
    # OpenCode (official global + Windows-friendly)
    (Join-Path $userHome ".config\opencode\skills"),
    (Join-Path $env:APPDATA "opencode\skills"),
    # Hermes
    (Join-Path $userHome ".hermes\skills"),
    # OpenClaw
    (Join-Path $userHome ".openclaw\skills")
  )
  $seen = @{}
  foreach ($c in $list) {
    if (-not $c) { continue }
    $key = $c.ToLowerInvariant()
    if ($seen.ContainsKey($key)) { continue }
    $seen[$key] = $true
    # Install if agent home already exists OR create for known product folders
    $parent = Split-Path $c -Parent
    $grand = if ($parent) { Split-Path $parent -Parent } else { $null }
    $known = ($parent -match 'opencode|hermes|openclaw|\.grok|\.claude|\.cursor|\.agents|\.codex')
    if ((Test-Path $parent) -or $known) {
      Write-Host "-> $c"
      Install-To $c
    }
    else {
      Write-Host "Skip (no agent root): $c"
    }
  }
}
else {
  $grok = Join-Path $env:USERPROFILE ".grok\skills"
  Write-Host "-> $grok (default; use -AllAgents for OpenCode/Hermes/OpenClaw/...)"
  Install-To $grok
}

if ($Project) {
  $cwd = Get-Location
  foreach ($c in @(
      (Join-Path $cwd ".grok\skills"),
      (Join-Path $cwd ".claude\skills"),
      (Join-Path $cwd ".cursor\skills"),
      (Join-Path $cwd ".agents\skills"),
      (Join-Path $cwd ".opencode\skills"),
      (Join-Path $cwd "skills")   # OpenClaw workspace-style
    )) {
    Write-Host "-> $c (project)"
    Install-To $c
  }
}

Write-Host ""
Write-Host "Done. Invocable skills (4):"
Write-Host "  /bcc-breaking-coding-chaos   (main)"
Write-Host "  /bcc-throughline"
Write-Host "  /bcc-plan-spar"
Write-Host "  /bcc-clean-cut"
Write-Host "New session recommended for each agent."
