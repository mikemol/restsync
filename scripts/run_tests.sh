#!/usr/bin/env bash
set -euo pipefail

test_dir="${TEST_ARTIFACTS_DIR:-artifacts/test_runs}"
mkdir -p "$test_dir"

if ! command -v mise >/dev/null 2>&1; then
  echo "mise is required. Install from https://mise.jdx.dev" >&2
  exit 1
fi

mise exec -- python -m pytest \
  --junitxml "$test_dir/junit.xml" \
  --log-file "$test_dir/pytest.log" \
  --log-file-level=INFO
