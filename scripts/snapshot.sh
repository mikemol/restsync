#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="${RESTSYNC_SNAPSHOT_DIR:-${repo_root}/artifacts/snapshots}"
mkdir -p "$output_dir"

stamp=$(date +%Y%m%d_%H%M%S)
output="$output_dir/restsync_snapshot_${stamp}.json"
restsync_bin="${RESTSYNC_BIN:-${repo_root}/.venv/bin/restsync}"
if [ ! -x "$restsync_bin" ]; then
  restsync_bin="${RESTSYNC_BIN:-restsync}"
fi

"$restsync_bin" snapshot --config "${RESTSYNC_CONFIG:-${repo_root}/configs/restsync.yml}" --output "$output"

echo "Snapshot written to $output"
