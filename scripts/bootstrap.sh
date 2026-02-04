#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v mise >/dev/null 2>&1; then
  echo "mise is required. Install from https://mise.jdx.dev" >&2
  exit 1
fi

mise install
mise exec -- python -m venv "${repo_root}/.venv"
"${repo_root}/.venv/bin/python" -m pip install --upgrade pip
"${repo_root}/.venv/bin/python" -m pip install -e "${repo_root}.[dev]"

echo "Bootstrap complete. Activate with: source ${repo_root}/.venv/bin/activate"
