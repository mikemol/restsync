#!/usr/bin/env bash
set -euo pipefail

output_dir="${RESTSYNC_PLAN_DIR:-artifacts/plan_runs}"
mkdir -p "$output_dir"

stamp=$(date +%Y%m%d_%H%M%S)
output="$output_dir/restsync_plan_${stamp}.json"

restsync plan --config "${RESTSYNC_CONFIG:-configs/restsync.yml}" --output "$output"

echo "Plan written to $output"
