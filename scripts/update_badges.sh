#!/usr/bin/env bash
set -euo pipefail

config="${RESTSYNC_CONFIG:-configs/restsync.yml}"
plan_dir="${RESTSYNC_PLAN_DIR:-artifacts/plan_runs}"
metrics_path="${RESTSYNC_METRICS_PATH:-$plan_dir/metrics.json}"
badge_path="${RESTSYNC_BADGE_PATH:-docs/badges/plan-health.json}"

mkdir -p "$plan_dir"
mkdir -p "$(dirname "$badge_path")"

restsync check \
  --config "$config" \
  --baseline baselines/overlay_baseline.json \
  --output "$plan_dir/plan.json" \
  --metrics "$metrics_path"

python scripts/metrics_badge.py --input "$metrics_path" --output "$badge_path"

echo "Badge written to $badge_path"
