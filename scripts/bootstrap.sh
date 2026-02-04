#!/usr/bin/env bash
set -euo pipefail

if ! command -v mise >/dev/null 2>&1; then
  echo "mise is required. Install from https://mise.jdx.dev" >&2
  exit 1
fi

mise install
mise exec -- python -m pip install --upgrade pip
mise exec -- python -m pip install -e .[dev]
