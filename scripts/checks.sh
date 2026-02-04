#!/usr/bin/env bash
set -euo pipefail

run_policy=true
run_docflow=true
run_dataflow=true
run_tests=true
list_only=false

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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
  $run_docflow && echo "- docflow (scripts/docflow_audit.py)" >&2
  $run_dataflow && echo "- dataflow (gabion check)" >&2
  $run_tests && echo "- tests (pytest)" >&2
  exit 0
fi

PYTHON_CMD=()
if [ -n "${RESTSYNC_PYTHON:-}" ]; then
  PYTHON_CMD=("$RESTSYNC_PYTHON")
elif [ -x "${repo_root}/.venv/bin/python" ]; then
  PYTHON_CMD=("${repo_root}/.venv/bin/python")
elif [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
  PYTHON_CMD=("${VIRTUAL_ENV}/bin/python")
elif command -v mise >/dev/null 2>&1; then
  PYTHON_CMD=(mise exec -- python)
else
  echo "python environment not found; set RESTSYNC_PYTHON, create .venv, activate venv, or install mise." >&2
  exit 1
fi

if $run_policy; then
  "${PYTHON_CMD[@]}" "${repo_root}/scripts/policy_check.py" --workflows
fi

if $run_docflow; then
  "${PYTHON_CMD[@]}" "${repo_root}/scripts/docflow_audit.py" --root "${repo_root}" --fail-on-violations
fi

if $run_dataflow; then
  report_dir="${DATAFLOW_REPORT_DIR:-${repo_root}/artifacts/audit_reports}"
  report_path="${DATAFLOW_REPORT_PATH:-$report_dir/dataflow_report.md}"
  mkdir -p "$report_dir"
  baseline_arg=()
  if [ -f "${repo_root}/baselines/dataflow_baseline.txt" ]; then
    baseline_arg+=(--baseline "${repo_root}/baselines/dataflow_baseline.txt")
  fi
  "${PYTHON_CMD[@]}" -m gabion check --report "$report_path" "${baseline_arg[@]}"
fi

if $run_tests; then
  test_dir="${TEST_ARTIFACTS_DIR:-${repo_root}/artifacts/test_runs}"
  mkdir -p "$test_dir"
  "${PYTHON_CMD[@]}" -m pytest \
    --junitxml "$test_dir/junit.xml" \
    --log-file "$test_dir/pytest.log" \
    --log-file-level=INFO
fi
