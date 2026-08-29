#!/usr/bin/env bash
#
# install-agents-skills.sh
#
# Install the agents and skills from this `prompts` repo into a workspace or
# the current user profile for GitHub Copilot (VS Code), OpenCode, and/or
# Claude Code.
#
# Usage:
#   ./install-agents-skills.sh <target> <platform> [options]
#
#   <target>    user | workspace
#   <platform>  copilot | opencode | claude | all
#
# Options:
#   --project <path>   project directory when <target>=workspace
#                      (default: current working directory)
#   --scope <scope>    what to install: agents | skills | all
#                      (default: all)
#   --dry-run          print what would be done without changing anything
#   --force            replace existing non-symlink targets with symlinks
#   -h, --help         show this help and exit
#
# Install locations (canonical for each tool):
#   copilot   workspace  <project>/.github/agents, <project>/.github/skills
#             user       ~/.copilot/agents,        ~/.copilot/skills
#   opencode  workspace  <project>/.opencode/agents, <project>/.opencode/skills
#             user       ~/.config/opencode/agents, ~/.config/opencode/skills
#   claude    workspace  <project>/.claude/agents,  <project>/.claude/skills
#             user       ~/.claude/agents,          ~/.claude/skills
#
# Examples:
#   # Install everything for all three tools into the user profile
#   ./install-agents-skills.sh user all
#
#   # Install claude agents + skills into a specific project
#   ./install-agents-skills.sh workspace claude --project ~/work/my-app
#
#   # Install only copilot skills into the current project
#   ./install-agents-skills.sh workspace copilot --scope skills
#
# Notes:
#   - Each whole source FOLDER is symlinked into place (never copied), so the
#     repo remains the source of truth: `git pull` in this repo updates every
#     installed agent and skill automatically. One symlink per destination:
#       <project>/.github/agents    -> prompts/copilot-agents
#       <project>/.github/skills    -> prompts/skills
#       <project>/.opencode/agents  -> prompts/opencode-agents
#       <project>/.opencode/skills  -> prompts/skills
#       <project>/.claude/agents    -> prompts/claude-agents
#       <project>/.claude/skills    -> prompts/skills
#   - Existing targets already linked to this repo are left alone (idempotent).
#   - If a target exists but is not one of our symlinks (e.g. an earlier
#     per-file install, or a directory holding unrelated files), it is skipped
#     with a warning; pass --force to replace it (the old target is deleted).
#   - If a skill destination already points at the source (e.g. ~/.copilot/skills
#     is a symlink to prompts/skills), skills are reported as already in sync
#     and left untouched.
#   - Agent folders must contain ONLY agent files (OpenCode registers every
#     *.md in the agents dir as an agent; VS Code/Claude skip non-agent files).
#     That is why opencode-agents/README.md was moved into README.md.
#   - Requires bash 3.2+ (works on stock macOS /usr/bin/bash).
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

TARGET=""
PLATFORM=""
PROJECT=""
SCOPE="all"
DRY_RUN=0
FORCE=0

# ---- helpers ---------------------------------------------------------------

usage() {
  awk 'NR > 1 && /^#/ { line = $0; sub(/^# ?/, "", line); print line }
       NR > 1 && !/^#/ { exit }' "$0"
}

die() {
  printf 'install-agents-skills: error: %s\n' "$*" >&2
  exit 1
}

info() { printf '  %s\n' "$*"; }

warn() { printf '  warning: %s\n' "$*" >&2; }

run_cmd() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

is_our_link() {
  # true if <link> is a symlink resolving to <src> — matches either the stored
  # link target string or the resolved directory path, so relative links and
  # equivalent absolute paths are recognized as already installed.
  local src="$1" link="$2"
  [ -L "$link" ] || return 1
  [ "$(readlink "$link")" = "$src" ] && return 0
  [ -d "$link" ] || return 1
  [ "$(cd -P "$link" 2>/dev/null && pwd -P)" = "$(cd -P "$src" && pwd -P)" ]
}

link_dir() {
  # Symlink the whole source directory <src> to <link>; idempotent — leaves our
  # own links alone, warns on foreign targets unless --force is set.
  local src="$1" link="$2"
  if [ -e "$link" ] || [ -L "$link" ]; then
    if is_our_link "$src" "$link"; then
      printf '  already linked    %s -> %s\n' "$link" "$src"
    elif [ "$FORCE" -eq 1 ]; then
      run_cmd rm -rf "$link"
      run_cmd ln -s "$src" "$link"
      printf '  relinked          %s -> %s\n' "$link" "$src"
    else
      warn "target '$link' exists and is not our symlink — skipped (use --force to replace; the existing directory would be deleted)"
    fi
    return
  fi
  run_cmd ln -s "$src" "$link"
  printf '  linked            %s -> %s\n' "$link" "$src"
}

# ---- source / destination mapping -----------------------------------------

platforms() {
  case "$PLATFORM" in
    all) printf '%s\n' copilot opencode claude ;;
    copilot|opencode|claude) printf '%s\n' "$PLATFORM" ;;
    *) die "unknown platform '$PLATFORM' (expected copilot, opencode, claude, or all)" ;;
  esac
}

agents_src() {
  case "$1" in
    copilot) printf '%s\n' "$SCRIPT_DIR/copilot-agents" ;;
    opencode) printf '%s\n' "$SCRIPT_DIR/opencode-agents" ;;
    claude) printf '%s\n' "$SCRIPT_DIR/claude-agents" ;;
  esac
}

agents_dest() {
  case "$1:$2" in
    copilot:user)      printf '%s\n' "$HOME/.copilot/agents" ;;
    copilot:workspace) printf '%s\n' "$PROJECT/.github/agents" ;;
    opencode:user)     printf '%s\n' "$HOME/.config/opencode/agents" ;;
    opencode:workspace) printf '%s\n' "$PROJECT/.opencode/agents" ;;
    claude:user)       printf '%s\n' "$HOME/.claude/agents" ;;
    claude:workspace)  printf '%s\n' "$PROJECT/.claude/agents" ;;
  esac
}

skills_dest() {
  case "$1:$2" in
    copilot:user)      printf '%s\n' "$HOME/.copilot/skills" ;;
    copilot:workspace) printf '%s\n' "$PROJECT/.github/skills" ;;
    opencode:user)     printf '%s\n' "$HOME/.config/opencode/skills" ;;
    opencode:workspace) printf '%s\n' "$PROJECT/.opencode/skills" ;;
    claude:user)       printf '%s\n' "$HOME/.claude/skills" ;;
    claude:workspace)  printf '%s\n' "$PROJECT/.claude/skills" ;;
  esac
}

same_path() {
  # true when two paths resolve to the same directory (follows symlinks)
  local a b
  a="$(cd "$1" 2>/dev/null && pwd -P)" || return 1
  b="$(cd "$2" 2>/dev/null && pwd -P)" || return 1
  [ "$a" = "$b" ]
}

# ---- install steps ---------------------------------------------------------

install_agents_for() {
  local platform="$1" src dst
  src="$(agents_src "$platform")"
  dst="$(agents_dest "$platform" "$TARGET")"
  [ -d "$src" ] || { warn "no agent sources at $src"; return; }

  run_cmd mkdir -p "$(dirname "$dst")"
  link_dir "$src" "$dst"
}

install_skills_for() {
  local platform="$1" dst
  dst="$(skills_dest "$platform" "$TARGET")"
  [ -d "$SKILLS_SRC" ] || { warn "no skills source at $SKILLS_SRC"; return; }

  if same_path "$SKILLS_SRC" "$dst"; then
    info "skills for $platform already in sync ($dst points at $SKILLS_SRC) — skipping"
    return
  fi

  run_cmd mkdir -p "$(dirname "$dst")"
  link_dir "$SKILLS_SRC" "$dst"
}

# ---- argument parsing ------------------------------------------------------

while [ "$#" -gt 0 ]; do
  case "$1" in
    user|workspace)
      TARGET="$1"
      ;;
    copilot|opencode|claude|all)
      PLATFORM="$1"
      ;;
    --project)
      [ "$#" -ge 2 ] || die "--project requires a value"
      PROJECT="$2"
      shift
      ;;
    --scope)
      [ "$#" -ge 2 ] || die "--scope requires a value"
      SCOPE="$2"
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    --force)
      FORCE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument '$1' (see --help)"
      ;;
  esac
  shift
done

[ -n "$TARGET" ] || die "missing <target> (user | workspace) — see --help"
[ -n "$PLATFORM" ] || die "missing <platform> (copilot | opencode | claude | all) — see --help"
case "$SCOPE" in
  agents|skills|all) ;;
  *) die "invalid --scope '$SCOPE' (expected agents, skills, or all)" ;;
esac

if [ "$TARGET" = workspace ]; then
  [ -n "$PROJECT" ] || PROJECT="$PWD"
  if [ "$DRY_RUN" -eq 0 ] && [ ! -d "$PROJECT" ]; then
    warn "project '$PROJECT' does not exist yet; directories will be created"
  fi
fi

printf 'Installing into %s profile for: %s\n' "$TARGET" "$PLATFORM"
if [ "$DRY_RUN" -eq 1 ]; then
  printf 'Dry run — no files will be changed.\n'
fi

for p in $(platforms); do
  printf '\n== %s ==\n' "$p"
  case "$SCOPE" in
    agents|all) install_agents_for "$p" ;;
  esac
  case "$SCOPE" in
    skills|all) install_skills_for "$p" ;;
  esac
done

printf '\nDone.\n'
