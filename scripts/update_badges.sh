#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config="${RESTSYNC_CONFIG:-${repo_root}/configs/restsync.yml}"
plan_dir="${RESTSYNC_PLAN_DIR:-${repo_root}/artifacts/plan_runs}"
metrics_path="${RESTSYNC_METRICS_PATH:-$plan_dir/metrics.json}"
badge_path="${RESTSYNC_BADGE_PATH:-${repo_root}/docs/badges/plan-health.json}"
restsync_bin="${RESTSYNC_BIN:-}"
python_bin="${RESTSYNC_PYTHON:-}"

if [ -z "$restsync_bin" ]; then
  if [ -x "${repo_root}/.venv/bin/restsync" ]; then
    restsync_bin="${repo_root}/.venv/bin/restsync"
  else
    restsync_bin="restsync"
  fi
fi

if [ -z "$python_bin" ]; then
  if [ -x "${repo_root}/.venv/bin/python" ]; then
    python_bin="${repo_root}/.venv/bin/python"
  else
    python_bin="python"
  fi
fi

mkdir -p "$plan_dir"
mkdir -p "$(dirname "$badge_path")"

"$restsync_bin" check \
  --config "$config" \
  --baseline "${repo_root}/baselines/overlay_baseline.json" \
  --output "$plan_dir/plan.json" \
  --metrics "$metrics_path"

"$python_bin" "${repo_root}/scripts/metrics_badge.py" --input "$metrics_path" --output "$badge_path"

echo "Badge written to $badge_path"
