#!/usr/bin/env bash
set -euo pipefail

run_policy=true
run_docflow=true
run_dataflow=false
run_tests=true
list_only=false

for arg in "$@"; do
  case "$arg" in
    --no-policy) run_policy=false ;;
    --policy-only) run_policy=true; run_docflow=false; run_dataflow=false; run_tests=false ;;
    --no-docflow) run_docflow=false ;;
    --docflow-only) run_docflow=true; run_policy=false; run_dataflow=false; run_tests=false ;;
    --dataflow) run_dataflow=true ;;
    --dataflow-only) run_dataflow=true; run_policy=false; run_docflow=false; run_tests=false ;;
    --tests-only) run_tests=true; run_policy=false; run_docflow=false; run_dataflow=false ;;
    --list) list_only=true ;;
    -h|--help)
      echo "Usage: scripts/checks.sh [--no-policy|--policy-only|--no-docflow|--docflow-only|--dataflow|--dataflow-only|--tests-only|--list]" >&2
      exit 0
      ;;
  esac
done

if $list_only; then
  echo "Checks to run:" >&2
  $run_policy && echo "- policy (scripts/policy_check.py --workflows)" >&2
  $run_docflow && echo "- docflow (gabion docflow-audit)" >&2
  $run_dataflow && echo "- dataflow (gabion check)" >&2
  $run_tests && echo "- tests (pytest)" >&2
  exit 0
fi

if ! command -v mise >/dev/null 2>&1; then
  echo "mise is required. Install from https://mise.jdx.dev" >&2
  exit 1
fi

if $run_policy; then
  mise exec -- python scripts/policy_check.py --workflows
fi

if $run_docflow; then
  mise exec -- python -m gabion docflow-audit --root . --fail-on-violations
fi

if $run_dataflow; then
  report_dir="${DATAFLOW_REPORT_DIR:-artifacts/audit_reports}"
  report_path="${DATAFLOW_REPORT_PATH:-$report_dir/dataflow_report.md}"
  mkdir -p "$report_dir"
  baseline_arg=()
  if [ -f baselines/dataflow_baseline.txt ]; then
    baseline_arg+=(--baseline baselines/dataflow_baseline.txt)
  fi
  mise exec -- python -m gabion check --report "$report_path" "${baseline_arg[@]}"
fi

if $run_tests; then
  test_dir="${TEST_ARTIFACTS_DIR:-artifacts/test_runs}"
  mkdir -p "$test_dir"
  mise exec -- python -m pytest \
    --junitxml "$test_dir/junit.xml" \
    --log-file "$test_dir/pytest.log" \
    --log-file-level=INFO
fi
