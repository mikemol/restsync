.PHONY: bootstrap check test plan snapshot policy docflow dataflow badges sync-actions clean-artifacts

bootstrap:
	@./scripts/bootstrap.sh

check:
	@./scripts/checks.sh

test:
	@mise exec -- python -m pytest

plan:
	@./scripts/plan_snapshot.sh

snapshot:
	@./scripts/snapshot.sh

policy:
	@mise exec -- python scripts/policy_check.py --workflows

docflow:
	@mise exec -- python scripts/docflow_audit.py --root . --fail-on-violations

dataflow:
	@mise exec -- python -m gabion check --report artifacts/audit_reports/dataflow_report.md

badges:
	@./scripts/update_badges.sh

sync-actions:
	@./scripts/sync_allowed_actions.py

clean-artifacts:
	@./scripts/clean_artifacts.sh
