#!/bin/sh
SCRIPTS_DIR=$(cd "$(dirname "$0")" && pwd)
CONFIG_DIR="$HOME/.config/pi-claude-md"
INSTALL_DIR="$CONFIG_DIR/git-hooks"
PREVIOUS_NAME_FILE="$CONFIG_DIR/pi-commit.previous-name"
HOOKS_PATH_SETTING='~/.config/pi-claude-md/git-hooks'
TEMPLATE_SETTING='~/.config/pi-claude-md/git-hooks/commit-template.txt'
CR=$(printf '\r')

fail() {
  printf 'pi-commit setup: %s\n' "$1" >&2
  exit 1
}

is_employee_code() {
  case $1 in
    [0-9][0-9][0-9][0-9]) return 0 ;;
  esac
  return 1
}

global() {
  git config --global "$@"
}

ask_code() {
  while :; do
    printf 'Employee code (4 digits): ' >&2
    read -r answer || fail "cancelled - nothing was changed"
    answer=${answer%"$CR"}
    is_employee_code "$answer" && { code=$answer; return; }
    printf 'Must be exactly 4 digits, e.g. 1234. Try again.\n' >&2
  done
}

confirm() {
  printf '\nCurrent git name : %s\nNew git name     : %s\nApply? [Y/n] ' "${current_name:-(not set)}" "$code" >&2
  read -r answer || fail "cancelled - nothing was changed"
  answer=${answer%"$CR"}
  case $answer in
    "" | y | Y | yes | YES) ;;
    *) fail "cancelled - nothing was changed" ;;
  esac
}

install() {
  command -v git >/dev/null || fail "git not found - install Git first: https://git-scm.com/downloads"
  current_hooks_path=$(global --get core.hooksPath)
  if [ -n "$current_hooks_path" ] && [ "$current_hooks_path" != "$HOOKS_PATH_SETTING" ]; then
    fail "core.hooksPath is already set to \"$current_hooks_path\" - nothing was changed.
Another tool owns your global git hooks. To replace it with pi-commit run:
  git config --global --unset core.hooksPath
then run setup again."
  fi
  current_name=$(global --get user.name)
  code=$1
  if [ -z "$code" ]; then
    ask_code
    confirm
  fi
  is_employee_code "$code" || fail "\"$code\" is not a 4-digit employee code - nothing was changed"

  mkdir -p "$INSTALL_DIR" || fail "cannot create $INSTALL_DIR"
  cp "$SCRIPTS_DIR/commit-msg" "$SCRIPTS_DIR/commit-template.txt" "$INSTALL_DIR/" || fail "cannot copy hook files to $INSTALL_DIR"
  chmod +x "$INSTALL_DIR/commit-msg"
  [ -f "$PREVIOUS_NAME_FILE" ] || printf '%s' "$current_name" > "$PREVIOUS_NAME_FILE"

  global user.name "$code"
  global core.hooksPath "$HOOKS_PATH_SETTING"
  current_template=$(global --get commit.template)
  if [ -z "$current_template" ] || [ "$current_template" = "$TEMPLATE_SETTING" ]; then
    global commit.template "$TEMPLATE_SETTING"
    template_status="commit.template   -> $TEMPLATE_SETTING"
  else
    template_status="commit.template   -> kept your own: $current_template"
  fi

  printf '\npi-commit installed\n  git user.name     -> %s\n  commit-msg hook   -> %s\n  %s\n\nCommit as usual, or use /pi-commit:commit in Claude Code.\n' \
    "$code" "$HOOKS_PATH_SETTING" "$template_status"
}

uninstall() {
  if [ -f "$PREVIOUS_NAME_FILE" ]; then
    previous_name=$(cat "$PREVIOUS_NAME_FILE")
    if [ -n "$previous_name" ]; then
      global user.name "$previous_name"
    else
      global --unset user.name
    fi
    rm -f "$PREVIOUS_NAME_FILE"
  fi
  [ "$(global --get core.hooksPath)" = "$HOOKS_PATH_SETTING" ] && global --unset core.hooksPath
  [ "$(global --get commit.template)" = "$TEMPLATE_SETTING" ] && global --unset commit.template
  rm -rf "$INSTALL_DIR"
  printf 'pi-commit removed. git user.name is now "%s".\n' "$(global --get user.name)"
}

status() {
  name=$(global --get user.name)
  hooks_path=$(global --get core.hooksPath)
  printf 'git user.name   : %s\ncore.hooksPath  : %s\ncommit-msg hook : %s\n' \
    "${name:-(not set)}" "${hooks_path:-(not set)}" "$([ -x "$INSTALL_DIR/commit-msg" ] && echo installed || echo missing)"
  is_employee_code "$name" && [ "$hooks_path" = "$HOOKS_PATH_SETTING" ] && [ -x "$INSTALL_DIR/commit-msg" ] || {
    printf 'Not set up - run /pi-commit:setup in Claude Code, or: sh "%s" install\n' "$0"
    exit 1
  }
  printf 'OK\n'
}

case ${1:-} in
  install) install "${2:-}" ;;
  uninstall) uninstall ;;
  status) status ;;
  *) fail "usage: sh setup.sh install [CODE] | uninstall | status" ;;
esac
