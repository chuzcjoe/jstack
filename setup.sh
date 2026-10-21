#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: setup.sh [--codex] [--claude] [--target PATH]

Configure J Mode and J Agent in the host project's root.
With no tool flags, configure both Codex and Claude Code.

  --codex        Configure Codex only, unless --claude is also given.
  --claude       Configure Claude Code only, unless --codex is also given.
  --target PATH  Use this Git project's root instead of detecting a superproject.
  -h, --help     Show this help.

Examples:
  ./vendor/jstack/setup.sh
  ./vendor/jstack/setup.sh --codex
  ./setup.sh --target /path/to/project --claude
EOF
}

fail() {
  printf 'setup.sh: %s\n' "$*" >&2
  exit 1
}

relative_path() {
  local base="$1" source="$2" prefix="" suffix
  while [[ "$source" != "$base" && "$source" != "$base/"* ]]; do
    [[ "$base" != / ]] || break
    base="${base%/*}"
    [[ -n "$base" ]] || base=/
    prefix="${prefix}../"
  done
  suffix="${source#"$base"}"
  suffix="${suffix#/}"
  printf '%s%s\n' "$prefix" "${suffix:-.}"
}

install_codex=0
install_claude=0
tool_selected=0
project_arg=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex) install_codex=1; tool_selected=1 ;;
    --claude) install_claude=1; tool_selected=1 ;;
    --target)
      [[ $# -ge 2 && -n "$2" && "$2" != --* ]] || fail '--target requires a project path.'
      project_arg="$2"
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown argument: $1. See --help." ;;
  esac
  shift
done

if [[ "$tool_selected" -eq 0 ]]; then
  install_codex=1
  install_claude=1
fi

command -v git >/dev/null 2>&1 || fail 'Git is required.'
jstack_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if [[ -n "$project_arg" ]]; then
  project_root="$(git -C "$project_arg" rev-parse --show-toplevel 2>/dev/null)" || fail "Not a Git project: $project_arg"
else
  project_root="$(git -C "$jstack_dir" rev-parse --show-superproject-working-tree 2>/dev/null || true)"
  [[ -n "$project_root" ]] || fail 'No superproject found. Add J Stack as a submodule or pass --target /path/to/project.'
fi
project_root="$(cd -- "$project_root" && pwd -P)"

sources=()
destinations=()
if [[ "$install_codex" -eq 1 ]]; then
  sources+=("$jstack_dir/skills/j-mode" "$jstack_dir/agents/j-agent.toml" "$jstack_dir/agents/j-agent.md")
  destinations+=("$project_root/.agents/skills/j-mode" "$project_root/.codex/agents/j-agent.toml" "$project_root/.codex/agents/j-agent.md")
fi
if [[ "$install_claude" -eq 1 ]]; then
  sources+=("$jstack_dir/skills/j-mode" "$jstack_dir/agents/j-agent.md")
  destinations+=("$project_root/.claude/skills/j-mode" "$project_root/.claude/agents/j-agent.md")
fi

[[ -f "$jstack_dir/skills/j-mode/SKILL.md" ]] || fail 'The J Mode skill is missing.'
for index in "${!sources[@]}"; do
  source="${sources[$index]}"
  destination="${destinations[$index]}"
  [[ -e "$source" ]] || fail "Missing source: $source"
  if [[ -e "$destination" || -L "$destination" ]]; then
    [[ -L "$destination" && "$destination" -ef "$source" ]] || fail "Conflict at $destination. Move the existing entry before rerunning setup."
  fi
  parent="$(dirname -- "$destination")"
  while [[ "$parent" != "$project_root" && "$parent" != / ]]; do
    if [[ -e "$parent" || -L "$parent" ]]; then
      [[ -d "$parent" ]] || fail "Expected a directory at $parent."
    fi
    parent="$(dirname -- "$parent")"
  done
done

for index in "${!sources[@]}"; do
  source="${sources[$index]}"
  destination="${destinations[$index]}"
  if [[ -L "$destination" && "$destination" -ef "$source" ]]; then
    printf 'Already configured: %s\n' "${destination#"$project_root"/}"
    continue
  fi
  mkdir -p -- "$(dirname -- "$destination")"
  parent="$(cd -- "$(dirname -- "$destination")" && pwd -P)"
  ln -s -- "$(relative_path "$parent" "$source")" "$destination"
  printf 'Linked: %s\n' "${destination#"$project_root"/}"
done

printf 'J Mode is configured in %s. Start a new agent session to load it.\n' "$project_root"
