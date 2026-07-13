#!/usr/bin/env bash
# Install BCC from a local clone: exactly 4 skills.
#
# Prefer the official one-liner when online (no clone needed):
#   npx skills add bo-cao/breaking-coding-chaos -g -y
# Claude Code plugin:
#   /plugin marketplace add bo-cao/breaking-coding-chaos
#   /plugin install bcc@breaking-coding-chaos
#
# This script is for Grok, offline, or custom paths:
#   ./install.sh              # ~/.grok/skills only
#   ./install.sh --all-agents # + Claude/Cursor/Codex/agents/OpenCode/Hermes/OpenClaw
#   ./install.sh --project    # project-local skill dirs
#   DEST=/path ./install.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/skills"
NAMES=(bcc-breaking-coding-chaos bcc-throughline bcc-plan-spar bcc-clean-cut)

install_to() {
  local target="$1"
  mkdir -p "$target"
  for obs in bcc bcc-status BCC-SESSION.md BCC-WRITEBACK.md SESSION.md WRITEBACK.md; do
    if [[ -e "$target/$obs" ]]; then
      rm -rf "$target/$obs"
      echo "  - removed obsolete $obs"
    fi
  done
  for n in "${NAMES[@]}"; do
    if [[ -d "$SRC/$n" ]]; then
      rm -rf "$target/$n"
      cp -R "$SRC/$n" "$target/$n"
      echo "  + $n"
    fi
  done
}

echo "BCC install from clone (4 skills only). Source: $SRC"
echo "Tip: online one-liner -> npx skills add bo-cao/breaking-coding-chaos -g -y"

if [[ -n "${DEST:-}" ]]; then
  echo "-> $DEST"
  install_to "$DEST"
elif [[ "${1:-}" == "--all-agents" ]]; then
  for c in \
    "$HOME/.grok/skills" \
    "$HOME/.claude/skills" \
    "$HOME/.cursor/skills" \
    "$HOME/.agents/skills" \
    "$HOME/.codex/skills" \
    "$HOME/.config/opencode/skills" \
    "$HOME/.hermes/skills" \
    "$HOME/.openclaw/skills"
  do
    parent="$(dirname "$c")"
    if [[ -d "$parent" ]] || [[ "$parent" == *opencode* || "$parent" == *hermes* || "$parent" == *openclaw* ]]; then
      echo "-> $c"
      install_to "$c"
    else
      echo "Skip: $c"
    fi
  done
else
  echo "-> $HOME/.grok/skills (default; use --all-agents for OpenCode/Hermes/OpenClaw/...)"
  install_to "$HOME/.grok/skills"
fi

if [[ "${1:-}" == "--project" ]] || [[ "${2:-}" == "--project" ]]; then
  for c in \
    "$(pwd)/.grok/skills" \
    "$(pwd)/.claude/skills" \
    "$(pwd)/.cursor/skills" \
    "$(pwd)/.agents/skills" \
    "$(pwd)/.opencode/skills" \
    "$(pwd)/skills"
  do
    echo "-> $c (project)"
    install_to "$c"
  done
fi

echo ""
echo "Done. Four skills: main + throughline + plan-spar + clean-cut"
