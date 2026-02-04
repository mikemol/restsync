#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_dir="${TEST_ARTIFACTS_DIR:-${repo_root}/artifacts/test_runs}"
mkdir -p "$test_dir"

PYTHON_CMD=()
if [ -n "${RESTSYNC_PYTHON:-}" ]; then
  PYTHON_CMD=("$RESTSYNC_PYTHON")
elif [ -x "${repo_root}/.venv/bin/python" ]; then
  PYTHON_CMD=("${repo_root}/.venv/bin/python")
elif [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
  PYTHON_CMD=("${VIRTUAL_ENV}/bin/python")
elif command -v mise >/dev/null 2>&1; then
  PYTHON_CMD=(mise exec -- python)
else
  echo "python environment not found; set RESTSYNC_PYTHON, create .venv, activate venv, or install mise." >&2
  exit 1
fi

"${PYTHON_CMD[@]}" -m pytest \
  --junitxml "$test_dir/junit.xml" \
  --log-file "$test_dir/pytest.log" \
  --log-file-level=INFO
