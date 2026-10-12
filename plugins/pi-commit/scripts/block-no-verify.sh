#!/bin/sh
BYPASS='--no-verify|core\.hooksPath|(^|[[:space:]"])-[aqsvm]*n[aqsvm]*([[:space:]"\\]|$)'
GIT_COMMIT='(^|[[:space:]"])git([[:space:]]+-[cC][[:space:]]+[^[:space:]]+|[[:space:]]+--?[a-zA-Z-]+(=[^[:space:]]+)?)*[[:space:]]+commit([[:space:]"\\]|$)'

if awk '{ gsub(/\\n|&&|\|\||;|\|/, "\n"); print }' | grep -E "$GIT_COMMIT" | grep -Eq -- "$BYPASS"; then
  echo "pi-commit: blocked. Do not skip the commit-msg hook (--no-verify, -n, core.hooksPath). Rewrite the message as \"type(scope): description\" and commit normally. If -n is part of the message text, reword it." >&2
  exit 2
fi
exit 0
