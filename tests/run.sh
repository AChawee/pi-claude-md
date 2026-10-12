#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v claude >/dev/null || { echo "ไม่พบคำสั่ง claude — ติดตั้ง Claude Code ก่อน" >&2; exit 1; }
PYTHON=${PYTHON:-$(command -v python3 || command -v python)}
claude plugin validate . --strict
claude plugin validate .claude --strict
for dir in plugins/*/ templates/plugin-template/; do
  claude plugin validate "$dir" --strict
done
"$PYTHON" -m unittest discover -s tests -v
echo "ALL TESTS PASSED"
