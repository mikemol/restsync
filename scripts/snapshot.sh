#!/usr/bin/env bash
set -euo pipefail

output_dir="${RESTSYNC_SNAPSHOT_DIR:-artifacts/snapshots}"
mkdir -p "$output_dir"

stamp=$(date +%Y%m%d_%H%M%S)
output="$output_dir/restsync_snapshot_${stamp}.json"

restsync snapshot --config "${RESTSYNC_CONFIG:-configs/restsync.yml}" --output "$output"

echo "Snapshot written to $output"
