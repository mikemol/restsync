#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="${RESTSYNC_PLAN_DIR:-${repo_root}/artifacts/plan_runs}"
mkdir -p "$output_dir"

stamp=$(date +%Y%m%d_%H%M%S)
output="$output_dir/restsync_plan_${stamp}.json"
metrics="$output_dir/restsync_metrics_${stamp}.json"
restsync_bin="${RESTSYNC_BIN:-${repo_root}/.venv/bin/restsync}"
if [ ! -x "$restsync_bin" ]; then
  restsync_bin="${RESTSYNC_BIN:-restsync}"
fi

"$restsync_bin" plan --config "${RESTSYNC_CONFIG:-${repo_root}/configs/restsync.yml}" --output "$output" --metrics "$metrics"

echo "Plan written to $output"
echo "Metrics written to $metrics"
